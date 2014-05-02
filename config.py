# config data
__author__ = 'cygairko'

MQTT_HOST = "archpi"
MQTT_PORT = 1883
MQTT_QOS = 2
DEVICE_ID = "raspi0"
SCOPE = "light"
SERVER_ID = "server0"

#Topics
MQTT_TOPIC_BASE = "home"
MQTT_SERVER_TOPIC = MQTT_TOPIC_BASE + "/" + DEVICE_ID + "/" + SERVER_ID
MQTT_REQUESTS_TOPIC = MQTT_TOPIC_BASE + "/+/" + DEVICE_ID + "/#"