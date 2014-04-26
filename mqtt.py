#!/usr/bin/python

# class for mqtt connection
__author__ = 'cygairko'

import json
import config
import paho.mqtt.client as mqtt
import light

led = light.Led()
led.start()


def on_connect(mosq, obj, rc):
    #mosq.subscribe("$SYS/#", 0)
    mosq.publish(config.MQTT_REGISTER_TOPIC, json.dumps({'function': 'register', 'scope': config.SCOPE, 'deviceid': config.DEVICE_ID}), config.MQTT_QOS)
    mosq.subscribe(config.MQTT_REQUEST_TOPIC, config.MQTT_QOS)

    print("rc: " + str(rc))


def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if (config.MQTT_REQUEST_TOPIC == msg.topic):
        messageString = msg.payload.decode("utf-8")
        decoded = json.loads(messageString)
        if (decoded['function'] == "setColor"):
            red = int(decoded['color'][0])
            green = int(decoded['color'][1])
            blue = int(decoded['color'][2])
            led.setColor(red, green, blue)

            # send ACK
            mosq.publish(config.MQTT_RESPONSE_TOPIC, messageString, config.MQTT_QOS)

        if (decoded['function'] == "getColor"):
            colors = led.getColor()
            mosq.publish(config.MQTT_RESPONSE_TOPIC, json.dumps({'response': 'getColor', 'color': [colors[0], colors[1], colors[2]]}), config.MQTT_QOS)


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mosquitto.Mosquitto("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect(config.MQTT_HOST, config.MQTT_PORT, 60)

#mqttc.subscribe(config.MQTT_ACT_TOPIC, 1)
#mqttc.publish("home/light/raspi0/response", "color123")

mqttc.loop_forever()