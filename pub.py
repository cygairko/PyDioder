#!/usr/bin/python
# simple script for publishing color into mqtt topic
__author__ = 'cygairko'

import paho.mqtt.client as mqtt
import config
import sys

mqttc = mqtt.Client()
mqttc.connect(config.MQTT_HOST, config.MQTT_PORT, 60)
color = sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3]
print(color)
mqttc.publish(config.MQTT_ACT_TOPIC, color, 1)
mqttc.disconnect()