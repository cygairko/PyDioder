# config data
__author__ = 'cygairko'

MQTT_HOST = 'archpi'
MQTT_PORT = 1883
MQTT_QOS = 2
DEVICE_ID = 'raspi0'
SCOPE = 'colorlight'
SERVER_ID = 'server0'

#Topics
MQTT_TOPIC_BASE = 'home'
MQTT_TOPIC_SERVER = MQTT_TOPIC_BASE + '/' + SERVER_ID
MQTT_TOPIC_REQUESTS = MQTT_TOPIC_BASE + '/' + DEVICE_ID + '/+'
MQTT_TOPIC_STATUSUPDATE = MQTT_TOPIC_SERVER + '/status'
MQTT_TOPIC_TESTAMENT = MQTT_TOPIC_SERVER + '/availability'