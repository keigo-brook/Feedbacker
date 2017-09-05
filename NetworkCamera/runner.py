# -*- coding: utf-8 -*-

import os
import json
import paho.mqtt.client as mqtt
import camera_mode_selector


# MQTT broker server
host = os.getenv('SSS_MQTT_HOST')
port = os.getenv('SSS_MQTT_PORT')

# subscribe topic
sub_topic = 'sensor/event'
# publish topic
pub_topic = 'sensor/feedback/result/'


def on_connect(client, data, flags, response_code):
    print('status {0}'.format(response_code))
    client.subscribe(sub_topic)


def on_message(client, data, msg):
    # msg.payload = { 'event' XX, 'changed': true }
    event = json.loads(msg.payload)['event']
    camera_mode_selector.change_mode(event)
    print('Received: {0} {1}'.format(msg.topic, msg.payload))


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
