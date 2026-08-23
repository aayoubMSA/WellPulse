#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-isrgrootx1.pem}"
URL="https://letsencrypt.org/certs/isrgrootx1.pem"
EXPECTED="96BCEC06264976F37460779ACF28C5A7CFE8A3C0AAE11A8FFCEE05C0BDDF08C6"

curl -fsSL "$URL" -o "$OUT"
ACTUAL=$(openssl x509 -in "$OUT" -noout -fingerprint -sha256 | sed 's/^.*=//' | tr -d ':\r\n' | tr '[:lower:]' '[:upper:]')
if [ "$ACTUAL" != "$EXPECTED" ]; then
  echo "ISRG Root X1 fingerprint mismatch" >&2
  rm -f "$OUT"
  exit 1
fi
openssl x509 -in "$OUT" -noout -subject -issuer -dates -fingerprint -sha256
