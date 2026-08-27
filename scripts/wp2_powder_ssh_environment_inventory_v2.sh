#!/usr/bin/env bash
set -euo pipefail

OUT=${1:?usage: wp2_powder_ssh_environment_inventory_v2.sh OUTDIR}
: "${CORE_USER:?}" "${CORE_HOST:?}" "${CORE_PORT:?}" "${UE_USER:?}" "${UE_HOST:?}" "${UE_PORT:?}"
mkdir -p "$OUT"

# Build a target source list and a THIRD-PARTY import list on the controller.
# Local modules and stdlib modules are deliberately excluded to avoid false positives.
python3 - "$OUT/third_party_imports.txt" "$OUT/sources.txt" <<'PY'
import ast, pathlib, sys
root=pathlib.Path('.')
files=[]
for p in list((root/'scripts').glob('wp2_*.py')) + list((root/'scripts').glob('wp_pwd01*.py')) + list((root/'src'/'wellpulse').glob('*.py')):
    if p.is_file(): files.append(p)
files=sorted(set(files))
local_roots={'wellpulse','scripts'} | {p.stem for p in files if p.parent.name=='scripts'}
stdlib=set(getattr(sys,'stdlib_module_names',()))
mods=set()
for p in files:
    try: tree=ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    except Exception: continue
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            for a in n.names: mods.add(a.name.split('.')[0])
        elif isinstance(n,ast.ImportFrom) and n.module:
            mods.add(n.module.split('.')[0])
third=sorted(m for m in mods if m not in local_roots and m not in stdlib and not m.startswith('_'))
pathlib.Path(sys.argv[1]).write_text('\n'.join(third)+'\n',encoding='utf-8')
pathlib.Path(sys.argv[2]).write_text('\n'.join(str(p) for p in files)+'\n',encoding='utf-8')
PY

python3 - "$OUT/third_party_imports.txt" "$OUT/sources.txt" "$OUT/remote_probe_v2.sh" <<'PY'
import json,pathlib,sys
third=[x.strip() for x in pathlib.Path(sys.argv[1]).read_text().splitlines() if x.strip()]
sources=[x.strip() for x in pathlib.Path(sys.argv[2]).read_text().splitlines() if x.strip()]
script=r'''#!/usr/bin/env bash
set -u
ROLE=${1:?role}
export PYTHONDONTWRITEBYTECODE=1
REPO="$HOME/WellPulse"
PINNED="$HOME/.wp2-golden-venv/bin/python"

echo "ROLE=$ROLE"
echo "HOST=$(hostname)"
echo "UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "UNAME=$(uname -a)"
if test -r /etc/os-release; then . /etc/os-release; echo "OS_ID=${ID:-unknown}"; echo "OS_VERSION=${VERSION_ID:-unknown}"; fi
if test -d "$REPO"; then echo 'REPO_PRESENT=yes'; else echo 'REPO_PRESENT=no'; fi
if test -d "$REPO/.git"; then
  printf 'REPO_SHA=%s\n' "$(git -C "$REPO" rev-parse HEAD 2>/dev/null || echo unknown)"
else
  echo 'REPO_SHA=NO_GIT_METADATA'
fi

emit_cli(){ name=$1; path=$(command -v "$name" 2>/dev/null || true); if test -z "$path"; then echo "CLI|$name|MISSING||"; return; fi; shift; ver=$("$@" 2>&1 | head -n 2 | tr '\n' ' ' || true); printf 'CLI|%s|PRESENT|%s|%s\n' "$name" "$path" "$ver"; }
emit_cli bash bash --version
emit_cli python3 python3 --version
emit_cli openssl openssl version
emit_cli tar tar --version
emit_cli sha256sum sha256sum --version
emit_cli find find --version
emit_cli sort sort --version
emit_cli xargs xargs --version
emit_cli rsync rsync --version
emit_cli curl curl --version
emit_cli git git --version
emit_cli jq jq --version
emit_cli java java -version
emit_cli javac javac -version
emit_cli mosquitto mosquitto -h
emit_cli mosquitto_pub mosquitto_pub -h
emit_cli mosquitto_sub mosquitto_sub -h

if command -v python3 >/dev/null 2>&1; then echo "SYSTEM_PYTHON=$(python3 --version 2>&1)"; else echo 'SYSTEM_PYTHON=MISSING'; fi
if test -x "$PINNED"; then
  echo "PINNED_PYTHON=$($PINNED --version 2>&1)"
  "$PINNED" - <<'PYCODE'
import importlib, importlib.metadata as md, json, sys
mods=__THIRD__
out={"executable":sys.executable,"version":sys.version,"imports":{},"distributions":{}}
for m in mods:
    try:
        importlib.import_module(m); out["imports"][m]={"ok":True}
    except Exception as e:
        out["imports"][m]={"ok":False,"error":type(e).__name__+":"+str(e)[:240]}
for dist in ("paho-mqtt","packaging"):
    try: out["distributions"][dist]=md.version(dist)
    except Exception as e: out["distributions"][dist]="MISSING:"+type(e).__name__
print("PINNED_JSON|"+json.dumps(out,sort_keys=True,separators=(",",":")))
PYCODE
  "$PINNED" -m pip freeze 2>/dev/null | sed 's/^/PINNED_FREEZE|/' || true
else
  echo 'PINNED_PYTHON=MISSING'
fi

# Compile with the exact target interpreter. Missing source is distinct from syntax failure.
if test -x "$PINNED" && test -d "$REPO"; then
  "$PINNED" - "$REPO" <<'PYCODE'
import pathlib,sys
repo=pathlib.Path(sys.argv[1]); sources=__SOURCES__
for rel in sources:
    p=repo/rel
    if not p.is_file(): print('SOURCE|MISSING|'+rel); continue
    try: compile(p.read_text(encoding='utf-8'),str(p),'exec'); print('SOURCE|SYNTAX_PASS|'+rel)
    except Exception as e: print('SOURCE|SYNTAX_FAIL|%s|%s:%s'%(rel,type(e).__name__,str(e)[:240]))
PYCODE
fi

for base in "$REPO" "$HOME/.m2" "$HOME"; do
  test -d "$base" || continue
  find "$base" -maxdepth 5 -type f \( -name '*paho*.jar' -o -name '*mqtt*.jar' \) -print 2>/dev/null | head -n 40 | while read -r j; do
    printf 'JAR|%s|%s\n' "$j" "$(sha256sum "$j" 2>/dev/null | awk '{print $1}')"
  done
done

echo "PROJ_WELLPULSE_PRESENT=$(test -d /proj/WellPulse && echo yes || echo no)"
echo "PROJ_WELLPULSE_WRITABLE=$(test -w /proj/WellPulse && echo yes || echo no)"
echo 'ROUTE_BEGIN'; ip route 2>&1 || true; echo 'ROUTE_END'
echo 'ADDR_BEGIN'; ip -br addr 2>&1 || true; echo 'ADDR_END'
'''
script=script.replace('__THIRD__',json.dumps(third)).replace('__SOURCES__',json.dumps(sources))
pathlib.Path(sys.argv[3]).write_text(script,encoding='utf-8')
PY
chmod 700 "$OUT/remote_probe_v2.sh"
bash -n "$OUT/remote_probe_v2.sh"

SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$HOME/.ssh/known_hosts")
probe_node(){
  local role=$1 user=$2 host=$3 port=$4
  echo "INVENTORY_V2_NODE_START=$role:$host:$port"
  ssh "${SSH_OPTS[@]}" -p "$port" "$user@$host" 'bash -s -- '"$role" < "$OUT/remote_probe_v2.sh" > "$OUT/$role-v2.txt" 2>&1
  grep -q '^PINNED_PYTHON=Python 3\.11\.13' "$OUT/$role-v2.txt" || { echo "INVENTORY_V2_BLOCKED=$role:PINNED_PYTHON"; return 20; }
  echo "INVENTORY_V2_NODE_PASS=$role"
}
probe_node core "$CORE_USER" "$CORE_HOST" "$CORE_PORT"
probe_node ue "$UE_USER" "$UE_HOST" "$UE_PORT"

python3 - "$OUT" <<'PY'
import json,pathlib,sys
root=pathlib.Path(sys.argv[1]); report={"schema":"wp2-powder-ssh-env-inventory-v2","nodes":{}}
for role in ('core','ue'):
    text=(root/(role+'-v2.txt')).read_text(errors='replace')
    node={"missing_cli":[],"third_party_import_failures":[],"source_missing":[],"source_syntax_failures":[],"jars":[]}
    for line in text.splitlines():
        if line.startswith('CLI|'):
            _,name,state,*_=line.split('|',4)
            if state=='MISSING': node['missing_cli'].append(name)
        elif line.startswith('PINNED_JSON|'):
            obj=json.loads(line[len('PINNED_JSON|'):]); node['pinned']=obj
            node['third_party_import_failures']=[k for k,v in obj.get('imports',{}).items() if not v.get('ok')]
        elif line.startswith('SOURCE|MISSING|'): node['source_missing'].append(line.split('|',2)[2])
        elif line.startswith('SOURCE|SYNTAX_FAIL|'): node['source_syntax_failures'].append(line)
        elif line.startswith('JAR|'):
            _,path,sha=line.split('|',2); node['jars'].append({"path":path,"sha256":sha})
        elif '=' in line and line.split('=',1)[0] in {'HOST','OS_ID','OS_VERSION','REPO_PRESENT','REPO_SHA','SYSTEM_PYTHON','PINNED_PYTHON','PROJ_WELLPULSE_PRESENT','PROJ_WELLPULSE_WRITABLE'}:
            k,v=line.split('=',1); node[k.lower()]=v
    report['nodes'][role]=node
(root/'inventory-v2.json').write_text(json.dumps(report,indent=2,sort_keys=True),encoding='utf-8')
PY

tar -C "$OUT" -cf "$OUT/wp2-powder-ssh-environment-inventory-v2.tar" third_party_imports.txt sources.txt core-v2.txt ue-v2.txt inventory-v2.json
sha256sum "$OUT/wp2-powder-ssh-environment-inventory-v2.tar" | tee "$OUT/archive-v2.sha256"
echo 'WP2_POWDER_SSH_ENV_INVENTORY_V2=PASS'
