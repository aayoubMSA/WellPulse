#!/usr/bin/env bash
set -euo pipefail

REQUEST="${1:-powder/g3-trigger-v3.json}"
TMP=/tmp/wellpulse-g3-v3
OUT=evidence/powder/g3-simstack-latest.md
RUNDEST="evidence/powder/g3/${GITHUB_RUN_ID:-manual}"
EXPECTED_AUTOMATION_FP='SHA256:jQGQvU86rtuEchT50N1HuB4Cmizpvbmp0zSBR4rowxY'
EXPECTED_PROFILE_ID='80dda605-7e5f-11e9-8006-e4434b2381fc'
EXPECTED_HARDWARE='d430'
EXPECTED_IMAGE_FRAGMENT='PowderProfiles:gnuradio-srslte'

mkdir -p "$TMP" "$RUNDEST"
TARGET_VALIDATED=0
PROCESS_GATE=FAIL
CLEANUP=NOT_ATTEMPTED
TX_RC=not_run
RX_RC=not_run
IQ_BYTES=0
IQ_SHA256=''
PROFILE_ID=not_captured
STATUS=unknown
EXPNAME=''
HOST=''
PORT=''
AUTOF=''
EXPID=''

write_evidence() {
  set +e
  local rundir="$TMP/wellpulse-g3-${GITHUB_RUN_ID:-manual}"
  if [[ -f "$rundir/result.env" ]]; then
    # shellcheck disable=SC1090
    source "$rundir/result.env"
    cp "$rundir/result.env" "$RUNDEST/result.env"
    cp "$rundir/remote-meta.txt" "$RUNDEST/remote-meta.txt" 2>/dev/null || true
    sed -E 's/\x1B\[[0-9;]*[mK]//g' "$rundir/tx.log" > "$RUNDEST/tx.log" 2>/dev/null || true
    sed -E 's/\x1B\[[0-9;]*[mK]//g' "$rundir/rx.log" > "$RUNDEST/rx.log" 2>/dev/null || true
  fi
  [[ -f "$TMP/manifest-summary.json" ]] && cp "$TMP/manifest-summary.json" "$RUNDEST/manifest-summary.json"
  [[ -f "$TMP/ssh-preflight.txt" ]] && cp "$TMP/ssh-preflight.txt" "$RUNDEST/ssh-preflight.txt"

  cat > "$OUT" <<EOF
# POWDER G3 simulated-stack validation — latest

- Checked UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- GitHub run ID: \`${GITHUB_RUN_ID:-manual}\`
- GitHub SHA: \`${GITHUB_SHA:-unknown}\`
- Orchestration mode: **MANUAL_CREATE_PLUS_AUTOMATED_ATTACH_V3**
- Evidence class: **INFRASTRUCTURE_ONLY_NON_SCORED**
- Experiment name: \`${EXPNAME}\`
- Experiment ID: \`${EXPID}\`
- Last observed portal status: \`${STATUS}\`
- Profile ID: \`${PROFILE_ID}\`
- SSH endpoint: \`${HOST}:${PORT}\`
- Automation public-key fingerprint: \`${AUTOF}\`
- Transmitter exit code: \`${TX_RC}\`
- Receiver exit code: \`${RX_RC}\`
- Generated simulated waveform bytes: \`${IQ_BYTES}\`
- Generated simulated waveform SHA-256: \`${IQ_SHA256}\`
- Process gate: **${PROCESS_GATE}**
- Cleanup gate: **${CLEANUP}**
- SDR/RF used: **NO**
- WellPulse/MQTT scientific workload used: **NO**

## Evidence boundary

This run validates only the profile-authoritative file-based simulated eNodeB-to-file-to-UE path on the manually provisioned POWDER experiment. It is not RF evidence and is not a scored WP-PWD01 run.
EOF

  cat > "$TMP/final.env" <<EOF
PROCESS_GATE=${PROCESS_GATE}
CLEANUP=${CLEANUP}
TARGET_VALIDATED=${TARGET_VALIDATED}
EOF
}

cleanup() {
  local original_rc=$?
  set +e
  if [[ "$TARGET_VALIDATED" -eq 1 && -n "$EXPID" ]]; then
    portal-cli experiment terminate --experiment-id "$EXPID" >"$TMP/terminate.out" 2>"$TMP/terminate.err"
    local term_rc=$?
    echo "Termination request rc=$term_rc"
    local misses=0
    local clean=0
    for _ in $(seq 1 30); do
      portal-cli experiment get --experiment-id "$EXPID" >"$TMP/postterm.json" 2>"$TMP/postterm.err"
      local get_rc=$?
      if [[ "$get_rc" -ne 0 ]]; then
        misses=$((misses+1))
        if [[ "$misses" -ge 3 ]]; then clean=1; break; fi
      else
        misses=0
        local st
        st="$(jq -r '.status // "unknown"' "$TMP/postterm.json" 2>/dev/null)"
        echo "Post-terminate status: $st"
        if [[ "$st" =~ ^(terminated|destroyed)$ ]]; then clean=1; break; fi
      fi
      sleep 5
    done
    if [[ "$clean" -eq 1 ]]; then CLEANUP=PASS; else CLEANUP=FAIL; fi
  else
    CLEANUP=NOT_ATTEMPTED_TARGET_NOT_VALIDATED
  fi
  write_evidence
  return "$original_rc"
}
trap cleanup EXIT

[[ -f "$REQUEST" ]] || { echo "Missing trigger request."; exit 2; }
EXPID="$(jq -r '.experiment_id // empty' "$REQUEST")"
EXECUTE="$(jq -r '.execute // empty' "$REQUEST")"
MODE="$(jq -r '.mode // empty' "$REQUEST")"
[[ "$EXPID" =~ ^[0-9a-fA-F-]{36}$ ]] || { echo "Invalid experiment UUID."; exit 2; }
[[ "$EXECUTE" == G3ATTACH ]] || { echo "Missing G3ATTACH authorization."; exit 2; }
[[ "$MODE" == ATTACH_ONLY_NO_RESOURCE_CREATE ]] || { echo "Wrong execution mode."; exit 2; }
[[ -n "${PORTAL_TOKEN:-}" && -n "${POWDER_USERNAME:-}" && -n "${POWDER_SSH_PRIVATE_KEY:-}" ]] || { echo "Required GitHub secret missing."; exit 2; }

echo "Attach-only G3 runner. No resource-creation command exists in this script."

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
umask 077
python3 - <<'PY'
import os
from pathlib import Path
s=os.environ['POWDER_SSH_PRIVATE_KEY']
if '\\n' in s and '\n' not in s:
    s=s.replace('\\n','\n')
s=s.replace('\r\n','\n').replace('\r','\n')
if not s.endswith('\n'):
    s+='\n'
Path.home().joinpath('.ssh/id_ed25519').write_text(s,encoding='utf-8',newline='\n')
PY
chmod 600 "$HOME/.ssh/id_ed25519"
: > "$HOME/.ssh/known_hosts"
chmod 600 "$HOME/.ssh/known_hosts"

ssh-keygen -y -P '' -f "$HOME/.ssh/id_ed25519" > "$TMP/automation.pub"
AUTOF="$(ssh-keygen -lf "$TMP/automation.pub" | awk '{print $2}')"
echo "Automation public-key fingerprint: $AUTOF"
[[ "$AUTOF" == "$EXPECTED_AUTOMATION_FP" ]] || { echo "Automation key fingerprint mismatch; refusing POWDER mutation."; exit 3; }

git clone --depth 1 https://gitlab.flux.utah.edu/emulab/portal-api.git /tmp/portal-api >/dev/null 2>&1
python -m pip install --quiet '/tmp/portal-api[cli]'

READY=0
for _ in $(seq 1 30); do
  set +e
  portal-cli experiment get --experiment-id "$EXPID" > "$TMP/status.json" 2> "$TMP/status.err"
  rc=$?
  set -e
  if [[ "$rc" -eq 0 ]]; then
    STATUS="$(jq -r '.status // "unknown"' "$TMP/status.json")"
    echo "POWDER status: $STATUS"
    if [[ "$STATUS" == ready ]]; then READY=1; break; fi
    [[ "$STATUS" =~ ^(failed|error|terminated|destroyed)$ ]] && { echo "Experiment is terminal: $STATUS"; exit 5; }
  fi
  sleep 10
done
[[ "$READY" -eq 1 ]] || { echo "Experiment did not reach/remain READY."; exit 6; }

portal-cli experiment manifests get --experiment-id "$EXPID" > "$TMP/manifests.json"
python3 - <<'PY'
import json, xml.etree.ElementTree as ET
from pathlib import Path
obj=json.loads(Path('/tmp/wellpulse-g3-v3/manifests.json').read_text())
xmls=[]
def walk(x):
    if isinstance(x,dict):
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
    elif isinstance(x,str) and '<' in x and 'rspec' in x.lower(): xmls.append(x)
walk(obj)
nodes=[]; logins=[]
for text in xmls:
    try: root=ET.fromstring(text)
    except Exception: continue
    for el in root.iter():
        if el.tag.rsplit('}',1)[-1] != 'node': continue
        n={'client_id':el.attrib.get('client_id',''),'component_id':el.attrib.get('component_id','')}
        for ch in el.iter():
            tag=ch.tag.rsplit('}',1)[-1]
            if tag=='hardware_type' and not n.get('hardware_type'): n['hardware_type']=ch.attrib.get('name','')
            elif tag=='disk_image' and not n.get('disk_image'): n['disk_image']=ch.attrib.get('name','')
            elif tag=='login' and ch.attrib.get('hostname'):
                logins.append({'username':ch.attrib.get('username',''),'hostname':ch.attrib['hostname'],'port':ch.attrib.get('port','22')})
        nodes.append(n)
uniq=[]; seen=set()
for x in logins:
    k=(x['username'],x['hostname'],x['port'])
    if k not in seen: seen.add(k); uniq.append(x)
summary={'nodes':nodes,'logins':uniq}
Path('/tmp/wellpulse-g3-v3/manifest-summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True))
if uniq: Path('/tmp/wellpulse-g3-v3/login.tsv').write_text(f"{uniq[0]['username']}\t{uniq[0]['hostname']}\t{uniq[0]['port']}\n")
PY

[[ -s "$TMP/login.tsv" ]] || { echo "No SSH endpoint in current manifest."; exit 7; }
PROFILE_ID="$(jq -r '.profile_id // empty' "$TMP/status.json")"
EXPNAME="$(jq -r '.name // .experiment_name // empty' "$TMP/status.json")"
EXP_PROJECT="$(jq -r '.project // .project_name // empty' "$TMP/status.json")"
HARDWARE="$(jq -r '.nodes[0].hardware_type // empty' "$TMP/manifest-summary.json")"
IMAGE="$(jq -r '.nodes[0].disk_image // empty' "$TMP/manifest-summary.json")"

echo "Portal profile ID: ${PROFILE_ID:-not_exposed}"
echo "Portal experiment name: ${EXPNAME:-not_exposed}"
echo "Portal project: ${EXP_PROJECT:-not_exposed}"
echo "Manifest hardware: $HARDWARE"
echo "Manifest image: $IMAGE"

if [[ -n "$PROFILE_ID" && "$PROFILE_ID" != "$EXPECTED_PROFILE_ID" ]]; then echo "Unexpected profile UUID."; exit 8; fi
[[ "$HARDWARE" == "$EXPECTED_HARDWARE" ]] || { echo "Unexpected hardware."; exit 8; }
[[ "$IMAGE" == *"$EXPECTED_IMAGE_FRAGMENT"* ]] || { echo "Unexpected image."; exit 8; }
[[ -z "$EXP_PROJECT" || "$EXP_PROJECT" == WellPulse ]] || { echo "Unexpected project."; exit 8; }
[[ -z "$EXPNAME" || "$EXPNAME" == WP-G3-SIMSTACK* ]] || { echo "Unexpected experiment name."; exit 8; }
TARGET_VALIDATED=1

IFS=$'\t' read -r MANIFEST_USER HOST PORT < "$TMP/login.tsv"
USERNAME="${MANIFEST_USER:-$POWDER_USERNAME}"
SSHOPTS=(-o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=2 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$HOME/.ssh/known_hosts" -i "$HOME/.ssh/id_ed25519" -p "$PORT")
SCPOPTS=(-o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$HOME/.ssh/known_hosts" -i "$HOME/.ssh/id_ed25519" -P "$PORT")
SSH_READY=0
for _ in $(seq 1 18); do
  if ssh "${SSHOPTS[@]}" "$USERNAME@$HOST" 'hostname; whoami' > "$TMP/ssh-preflight.txt" 2> "$TMP/ssh-preflight.err"; then SSH_READY=1; break; fi
  sleep 10
done
[[ "$SSH_READY" -eq 1 ]] || { echo "SSH never became ready."; exit 9; }

scp "${SCPOPTS[@]}" powder/g3_simstack_remote.sh "$USERNAME@$HOST:/tmp/wellpulse_g3_simstack.sh"
ssh "${SSHOPTS[@]}" "$USERNAME@$HOST" "chmod 700 /tmp/wellpulse_g3_simstack.sh && /tmp/wellpulse_g3_simstack.sh '${GITHUB_RUN_ID:-manual}'" > "$TMP/remote-run.out" 2> "$TMP/remote-run.err"
scp -r "${SCPOPTS[@]}" "$USERNAME@$HOST:/tmp/wellpulse-g3-${GITHUB_RUN_ID:-manual}" "$TMP/"
ssh "${SSHOPTS[@]}" "$USERNAME@$HOST" "rm -rf /tmp/wellpulse-g3-${GITHUB_RUN_ID:-manual} /tmp/wellpulse_g3_simstack.sh" >/dev/null 2>&1 || true

RUNDIR="$TMP/wellpulse-g3-${GITHUB_RUN_ID:-manual}"
[[ -f "$RUNDIR/result.env" ]] || { echo "Missing remote result.env."; exit 10; }
# shellcheck disable=SC1090
source "$RUNDIR/result.env"
[[ "$PROCESS_GATE" == PASS && "$TX_RC" -eq 0 && "$RX_RC" -eq 0 && "$IQ_BYTES" -gt 0 ]] || { echo "G3 process gate failed."; exit 11; }
echo "G3 process candidate PASS: TX_RC=$TX_RC RX_RC=$RX_RC IQ_BYTES=$IQ_BYTES"
