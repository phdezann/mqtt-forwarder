#!/usr/bin/env bash

set -e -u -x

sudo apt-get install -y mosquitto mosquitto-clients
python3 -m pip install paho-mqtt

python3 main.py \
  --src-mqtt-server="${SRC_MQTT_HOSTNAME}" \
  --dst-mqtt-server="${DST_MQTT_HOSTNAME}" \
  --topic="${TOPIC}" \
  "$@"
