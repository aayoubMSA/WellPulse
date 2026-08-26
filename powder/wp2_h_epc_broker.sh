#!/usr/bin/env bash
set -euo pipefail

WORKDIR="${1:-/tmp/wellpulse-wp2-h-broker}"
mkdir -p "$WORKDIR"
chmod 700 "$WORKDIR"

if ! command -v openssl >/dev/null 2>&1; then
  echo "BLOCKED: openssl is required" >&2
  exit 12
fi

if ! command -v mosquitto >/dev/null 2>&1; then
  if [[ "${WP_ALLOW_APT_INSTALL:-0}" == "1" ]] && command -v sudo >/dev/null 2>&1; then
    sudo apt-get update -qq
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq mosquitto
  else
    echo "BLOCKED: mosquitto is not installed. Re-run with WP_ALLOW_APT_INSTALL=1 if ephemeral package installation is authorized." >&2
    exit 13
  fi
fi

cat > "$WORKDIR/ca.cnf" <<'EOF'
[req]
prompt = no
distinguished_name = dn
x509_extensions = v3_ca
[dn]
CN = WellPulse WP2 H Calibration Ephemeral CA
[v3_ca]
basicConstraints = critical,CA:TRUE
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
EOF

cat > "$WORKDIR/server.cnf" <<'EOF'
[req]
prompt = no
distinguished_name = dn
req_extensions = req_ext
[dn]
CN = 172.16.0.1
[req_ext]
subjectAltName = @alt_names
[alt_names]
IP.1 = 172.16.0.1
EOF

cat > "$WORKDIR/server-ext.cnf" <<'EOF'
basicConstraints = CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = IP:172.16.0.1
EOF

umask 077
openssl genrsa -out "$WORKDIR/ca.key" 2048 >/dev/null 2>&1
openssl req -x509 -new -key "$WORKDIR/ca.key" -sha256 -days 1 \
  -out "$WORKDIR/ca.crt" -config "$WORKDIR/ca.cnf" >/dev/null 2>&1
openssl genrsa -out "$WORKDIR/server.key" 2048 >/dev/null 2>&1
openssl req -new -key "$WORKDIR/server.key" -out "$WORKDIR/server.csr" \
  -config "$WORKDIR/server.cnf" >/dev/null 2>&1
openssl x509 -req -in "$WORKDIR/server.csr" -CA "$WORKDIR/ca.crt" -CAkey "$WORKDIR/ca.key" \
  -CAcreateserial -out "$WORKDIR/server.crt" -days 1 -sha256 \
  -extfile "$WORKDIR/server-ext.cnf" >/dev/null 2>&1
chmod 600 "$WORKDIR/ca.key" "$WORKDIR/server.key"
chmod 644 "$WORKDIR/ca.crt" "$WORKDIR/server.crt"

cat > "$WORKDIR/mosquitto.conf" <<EOF
listener 8883 0.0.0.0
allow_anonymous true
persistence false
certfile $WORKDIR/server.crt
keyfile $WORKDIR/server.key
log_type all
EOF

if [[ -f "$WORKDIR/mosquitto.pid" ]]; then
  OLD_PID="$(cat "$WORKDIR/mosquitto.pid" 2>/dev/null || true)"
  if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
    kill "$OLD_PID" || true
    sleep 1
  fi
fi

nohup mosquitto -c "$WORKDIR/mosquitto.conf" -v > "$WORKDIR/mosquitto.log" 2>&1 &
echo $! > "$WORKDIR/mosquitto.pid"

READY=0
for _ in $(seq 1 30); do
  if ss -ltn 2>/dev/null | grep -qE '[:.]8883[[:space:]]'; then
    READY=1
    break
  fi
  sleep 0.5
done

if [[ "$READY" != "1" ]]; then
  echo "BLOCKED: MQTT TLS broker did not open port 8883" >&2
  tail -n 80 "$WORKDIR/mosquitto.log" >&2 || true
  exit 14
fi

CA_SHA="$(sha256sum "$WORKDIR/ca.crt" | awk '{print $1}')"
CERT_SHA="$(sha256sum "$WORKDIR/server.crt" | awk '{print $1}')"
NOT_AFTER="$(openssl x509 -in "$WORKDIR/server.crt" -noout -enddate | sed 's/^notAfter=//')"
cat > "$WORKDIR/broker_public.json" <<EOF
{
  "evidence_class": "NON_SCORED_WP2_H_CALIBRATION",
  "listen_ip": "0.0.0.0",
  "listen_port": 8883,
  "tls": true,
  "server_identity": "172.16.0.1",
  "ca_cert_sha256": "$CA_SHA",
  "server_cert_sha256": "$CERT_SHA",
  "server_cert_not_after": "$NOT_AFTER",
  "authentication": "anonymous_ephemeral_isolated_experiment",
  "private_key_preserved_in_evidence": false
}
EOF

printf 'BROKER_READY=1\n'
printf 'CA_CERT=%s\n' "$WORKDIR/ca.crt"
printf 'BROKER_PUBLIC=%s\n' "$WORKDIR/broker_public.json"
