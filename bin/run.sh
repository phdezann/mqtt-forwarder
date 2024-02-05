#!/usr/bin/env bash

set -e -u -x

sudo apt-get install -y mosquitto mosquitto-clients
python3 -m pip install paho-mqtt

cmd="python3 main.py"
cmd="${cmd} --src-mqtt-server=${SRC_MQTT_HOSTNAME}"

if [ -n "${SRC_MQTT_PORT:-}" ]; then
  cmd="${cmd} --src-mqtt-port=${SRC_MQTT_PORT}"
fi

if [ -n "${SRC_MQTT_USERNAME:-}" ]; then
  cmd="${cmd} --src-mqtt-username=${SRC_MQTT_USERNAME}"
fi

if [ -n "${SRC_MQTT_PASSWORD:-}" ]; then
  cmd="${cmd} --src-mqtt-password=${SRC_MQTT_PASSWORD}"
fi

cmd="${cmd} --dst-mqtt-server=${DST_MQTT_HOSTNAME}"

if [ -n "${DST_MQTT_PORT:-}" ]; then
  cmd="${cmd} --dst-mqtt-port=${DST_MQTT_PORT}"
fi

if [ -n "${DST_MQTT_USERNAME:-}" ]; then
  cmd="${cmd} --dst-mqtt-username=${DST_MQTT_USERNAME}"
fi

if [ -n "${DST_MQTT_PASSWORD:-}" ]; then
  cmd="${cmd} --dst-mqtt-password=${DST_MQTT_PASSWORD}"
fi

cmd="${cmd} --topic=${TOPIC}"

${cmd} "$@"
