#!/usr/bin/env bash
set -euo pipefail

OUT=${1:?usage: wp2_powder_ssh_environment_inventory.sh OUTDIR}
: "${CORE_USER:?}" "${CORE_HOST:?}" "${CORE_PORT:?}" "${UE_USER:?}" "${UE_HOST:?}" "${UE_PORT:?}"
mkdir -p "$OUT"

# Build a broad import closure from WP2/P7B Python sources without importing project code locally.
python3 - "$OUT/imports.txt" "$OUT/sources.txt" <<'PY'
import ast, pathlib, sys
root=pathlib.Path('.')
files=[]
for p in list((root/'scripts').glob('wp2_*.py')) + list((root/'scripts').glob('wp_pwd01*.py')) + list((root/'src'/'wellpulse').glob('*.py')):
    if p.is_file(): files.append(p)
mods=set()
for p in sorted(set(files)):
    try: tree=ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    except Exception: continue
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            for a in n.names: mods.add(a.name)
        elif isinstance(n,ast.ImportFrom) and n.module:
            mods.add(n.module)
pathlib.Path(sys.argv[1]).write_text('\n'.join(sorted(mods))+'\n',encoding='utf-8')
pathlib.Path(sys.argv[2]).write_text('\n'.join(str(p) for p in sorted(set(files)))+'\n',encoding='utf-8')
PY

# Remote probe is generated once and piped over SSH; it does not write to POWDER nodes.
python3 - "$OUT/imports.txt" "$OUT/sources.txt" "$OUT/remote_probe.sh" <<'PY'
import json, pathlib, shlex, sys
mods=[x.strip() for x in pathlib.Path(sys.argv[1]).read_text().splitlines() if x.strip()]
sources=[x.strip() for x in pathlib.Path(sys.argv[2]).read_text().splitlines() if x.strip()]
mods_json=json.dumps(mods)
sources_json=json.dumps(sources)
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
echo "REPO_PRESENT=$(test -d \"$REPO\" && echo yes || echo no)"
if test -d "$REPO/.git"; then echo "REPO_SHA=$(git -C \"$REPO\" rev-parse HEAD 2>/dev/null || echo unknown)"; fi
for c in bash python python3 pip pip3 java javac openssl mosquitto mosquitto_pub mosquitto_sub tar sha256sum find sort xargs rsync tmux ss pgrep curl jq ip ping timeout awk sed grep stat date git; do
  if command -v "$c" >/dev/null 2>&1; then
    p=$(command -v "$c")
    v=$(("$c" --version 2>&1 || "$c" -version 2>&1 || "$c" -V 2>&1 || true) | head -n 2 | tr '\n' ' ')
    printf 'CLI|%s|PRESENT|%s|%s\n' "$c" "$p" "$v"
  else
    printf 'CLI|%s|MISSING||\n' "$c"
  fi
done

probe_py(){
  label=$1; py=$2
  if ! test -x "$py" && ! command -v "$py" >/dev/null 2>&1; then echo "PYTHON|$label|MISSING"; return 0; fi
  resolved=$(command -v "$py" 2>/dev/null || printf '%s' "$py")
  echo "PYTHON|$label|PATH|$resolved"
  "$py" - <<'PYCODE'
import importlib, json, os, platform, sys
mods=__MODS__
out={"version":sys.version,"executable":sys.executable,"platform":platform.platform(),"imports":{}}
for m in mods:
    root=m.split('.')[0]
    if root in {"wellpulse","scripts"}: continue
    try:
        importlib.import_module(m)
        out["imports"][m]={"ok":True}
    except Exception as e:
        out["imports"][m]={"ok":False,"error":type(e).__name__+":"+str(e)[:240]}
try:
    import pkg_resources
    out["distributions"]=sorted([{"name":d.project_name,"version":d.version} for d in pkg_resources.working_set], key=lambda x:x["name"].lower())
except Exception as e:
    out["distributions_error"]=type(e).__name__+":"+str(e)
print("PYJSON|"+json.dumps(out,sort_keys=True,separators=(",",":")))
PYCODE
  "$py" -m pip freeze 2>/dev/null | sed "s/^/PIPFREEZE|$label|/" || true
}
probe_py system python3
probe_py pinned "$PINNED"

# Compile the exact WP2/P7B source set using the pinned interpreter, without imports or pyc writes.
if test -x "$PINNED" && test -d "$REPO"; then
  "$PINNED" - "$REPO" <<'PYCODE'
import json, pathlib, sys
repo=pathlib.Path(sys.argv[1]); sources=__SOURCES__
for rel in sources:
    p=repo/rel
    if not p.is_file():
        print("SOURCE|MISSING|"+rel); continue
    try:
        compile(p.read_text(encoding="utf-8"),str(p),"exec")
        print("SOURCE|SYNTAX_PASS|"+rel)
    except Exception as e:
        print("SOURCE|SYNTAX_FAIL|%s|%s:%s"%(rel,type(e).__name__,str(e)[:240]))
PYCODE
fi

# Java/MQTT jars and hashes, read-only.
for base in "$REPO" "$HOME/.m2" "$HOME"; do
  test -d "$base" || continue
  find "$base" -maxdepth 5 -type f \( -name '*paho*.jar' -o -name '*mqtt*.jar' \) -print 2>/dev/null | head -n 40 | while read -r j; do
    printf 'JAR|%s|%s\n' "$j" "$(sha256sum "$j" 2>/dev/null | awk '{print $1}')"
  done
done

echo "PROJ_WELLPULSE_PRESENT=$(test -d /proj/WellPulse && echo yes || echo no)"
echo "PROJ_WELLPULSE_WRITABLE=$(test -w /proj/WellPulse && echo yes || echo no)"
echo "ROUTE_BEGIN"; ip route 2>&1 || true; echo "ROUTE_END"
echo "ADDR_BEGIN"; ip -br addr 2>&1 || true; echo "ADDR_END"
'''
script=script.replace('__MODS__',mods_json).replace('__SOURCES__',sources_json)
pathlib.Path(sys.argv[3]).write_text(script,encoding='utf-8')
PY
chmod 700 "$OUT/remote_probe.sh"

SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$HOME/.ssh/known_hosts")
probe_node(){
  local role=$1 user=$2 host=$3 port=$4
  echo "INVENTORY_NODE_START=$role:$host:$port"
  ssh "${SSH_OPTS[@]}" -p "$port" "$user@$host" 'bash -s -- '"$role" < "$OUT/remote_probe.sh" > "$OUT/$role.txt" 2>&1
  grep -q '^PYTHON|pinned|' "$OUT/$role.txt" || { echo "INVENTORY_NODE_BLOCKED=$role:PINNED_PYTHON_NOT_OBSERVED"; return 20; }
  echo "INVENTORY_NODE_PASS=$role"
}
probe_node core "$CORE_USER" "$CORE_HOST" "$CORE_PORT"
probe_node ue "$UE_USER" "$UE_HOST" "$UE_PORT"

python3 - "$OUT" <<'PY'
import json,pathlib,re,sys
root=pathlib.Path(sys.argv[1]); report={"schema":"wp2-powder-ssh-env-inventory-v1","nodes":{}}
for role in ("core","ue"):
    text=(root/(role+'.txt')).read_text(errors='replace')
    node={"raw_file":role+'.txt',"missing_cli":[],"python":{},"source_syntax_failures":[],"jars":[]}
    for line in text.splitlines():
        if line.startswith('CLI|'):
            _,name,state,*rest=line.split('|',4)
            if state=='MISSING': node['missing_cli'].append(name)
        elif line.startswith('PYTHON|') and '|PATH|' in line:
            _,label,_,path=line.split('|',3); node['python'].setdefault(label,{})['path']=path
        elif line.startswith('PYJSON|'):
            obj=json.loads(line[len('PYJSON|'):]); label='pinned' if obj.get('executable','').endswith('/.wp2-golden-venv/bin/python') else 'system'; node['python'][label]=obj
        elif line.startswith('SOURCE|SYNTAX_FAIL|'):
            node['source_syntax_failures'].append(line)
        elif line.startswith('JAR|'):
            _,path,sha=line.split('|',2); node['jars'].append({"path":path,"sha256":sha})
        elif '=' in line and line.split('=',1)[0] in {'HOST','UNAME','OS_ID','OS_VERSION','REPO_SHA','PROJ_WELLPULSE_PRESENT','PROJ_WELLPULSE_WRITABLE'}:
            k,v=line.split('=',1); node[k.lower()]=v
    report['nodes'][role]=node
(root/'inventory.json').write_text(json.dumps(report,indent=2,sort_keys=True),encoding='utf-8')
PY

tar -C "$OUT" -cf "$OUT/wp2-powder-ssh-environment-inventory.tar" imports.txt sources.txt core.txt ue.txt inventory.json
sha256sum "$OUT/wp2-powder-ssh-environment-inventory.tar" | tee "$OUT/archive.sha256"
echo 'WP2_POWDER_SSH_ENV_INVENTORY=PASS'
