# config data
__author__ = 'cygairko'

MQTT_HOST = "archpi"
MQTT_PORT = 1883
MQTT_QOS = 2
DEVICE_ID = "raspi0"
SCOPE = "light"

#Topics
MQTT_REGISTER_TOPIC = "home/server/register"
MQTT_REQUEST_TOPIC = "home/" + SCOPE + "/" + DEVICE_ID + "/request"
MQTT_RESPONSE_TOPIC = "home/" + SCOPE + "/" + DEVICE_ID + "/response"