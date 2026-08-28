#!/usr/bin/env bash
set -euo pipefail

ROLE=${1:?usage: wp2_powder_fresh_node_init.sh core|ue}
case "$ROLE" in core|ue) ;; *) echo "INIT=BLOCKED:BAD_ROLE"; exit 2;; esac

REPO=${WP_REPO_ROOT:-$HOME/WellPulse}
JAR=/tmp/wp2-p7b-rq2-paho.jar
JAR_URL='https://repo.maven.apache.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/org.eclipse.paho.client.mqttv3-1.2.5.jar'
JAR_SHA='59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185'

cd "$REPO"

sudo apt-get update -qq
if [[ "$ROLE" == core ]]; then
  sudo apt-get install -y mosquitto mosquitto-clients
  sudo systemctl start mosquitto
else
  sudo apt-get install -y openjdk-11-jre-headless mosquitto-clients
fi

bash scripts/wp2_a3_runtime_bootstrap.sh

if [[ "$ROLE" == ue ]]; then
  curl -fsSL "$JAR_URL" -o "$JAR"
  printf '%s  %s\n' "$JAR_SHA" "$JAR" | sha256sum -c -
  WP_B2_JAR_PATH="$JAR" bash scripts/wp2_p7b_target_node_preflight.sh ue
else
  bash scripts/wp2_p7b_target_node_preflight.sh core
fi

echo "WP2_POWDER_FRESH_NODE_INIT=PASS:$ROLE"
