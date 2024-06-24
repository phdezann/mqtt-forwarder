import logging
import signal
import sys
from argparse import ArgumentParser

from mqtt.mqtt_monitor import MqttClientMonitor, TerminationStatus
from mqtt.mqtt_pub import MqttPub
from mqtt.mqtt_sub import MqttSub

QOS = 2

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


def main(args):
    monitor = MqttClientMonitor()
    publisher = MqttPub(monitor, args.dst_mqtt_server, args.dst_mqtt_port, args.topic, QOS,
                        mqtt_username=args.dst_mqtt_username,
                        mqtt_password=args.dst_mqtt_password)

    def on_message(msg, topic):
        publisher.publish(msg)
        logging.debug(
            f"Message '{msg}' forwarded "
            f"from {args.src_mqtt_server} to {args.dst_mqtt_server} on topic {topic}")

    subscriber = MqttSub(monitor, args.src_mqtt_server, args.src_mqtt_port, args.topic, QOS, on_message,
                         mqtt_username=args.src_mqtt_username,
                         mqtt_password=args.src_mqtt_password)

    publisher.start()
    subscriber.start()

    def signal_handler(_1, _2):
        monitor.terminate_all()

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logging.info("Mqtt forwarder is now ready")
    status = monitor.wait_for_termination()
    monitor.close_all_clients(status)
    return status


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--src-mqtt-server", required=True)
    parser.add_argument("--src-mqtt-port", type=int, default=1883)
    parser.add_argument("--src-mqtt-username")
    parser.add_argument("--src-mqtt-password")
    parser.add_argument("--dst-mqtt-server", required=True)
    parser.add_argument("--dst-mqtt-port", type=int, default=1883)
    parser.add_argument("--dst-mqtt-username")
    parser.add_argument("--dst-mqtt-password")
    parser.add_argument("--topic", required=True)
    args = parser.parse_args()

    termination_status = main(args)

    if termination_status == TerminationStatus.NORMAL_TERMINATION:
        sys.exit(0)
    elif termination_status == TerminationStatus.ABNORMAL_TERMINATION:
        sys.exit(1)
