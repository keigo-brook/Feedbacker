# -*- coding: utf-8 -*-

import os
import json
import paho.mqtt.client as mqtt
import camera_mode_selector
from logging import getLogger, FileHandler, StreamHandler, DEBUG
logger = getLogger(__name__)
if not logger.handlers:
    fileHandler = FileHandler(r'./log/camera_runner.log')
    fileHandler.setLevel(DEBUG)
    streamHander = StreamHandler()
    streamHander.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHander)


# MQTT broker server
host = os.getenv('SSS_MQTT_HOST')
port = int(os.getenv('SSS_MQTT_PORT'))

# subscribe topic
sub_topic = 'sensor/event'
# publish topic
pub_topic = 'sensor/feedback/result/'


def on_connect(client, data, flags, response_code):
    logger.info('status {0}'.format(response_code))
    camera_mode_selector.change_mode('2')
    client.subscribe(sub_topic)


def on_message(client, data, msg):
    # msg.payload = { 'event' XX, 'changed': true }
    logger.info('Received: {0} {1}'.format(msg.topic, msg.payload))
    payload = msg.payload.decode('utf8').replace("'", '"')
    event = json.loads(payload)
    if event['changed']:
        camera_mode_selector.change_mode(event['event'])


def main():
    """
    subscribe: sensor/feedback/tilt
    publish: sensor/feedback/result

    フィードバック命令を受信，フィードバックを行う
    """

    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port=port, keepalive=60)
    client.loop_forever()


if __name__ == '__main__':
    main()
