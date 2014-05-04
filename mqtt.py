#!/usr/bin/python

# class for mqtt connection
__author__ = 'cygairko'

import json
import signal
import sys
import time
import re

import config
import light


try:
    import paho.mqtt.client as mqtt
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.client"
    import os
    import inspect

    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt

led = light.Led()
led.start()

retained = True
notretained = False

pattern = re.compile(config.MQTT_TOPIC_BASE + '/([a-z0-9]+)/([a-z0-9]+)/([a-z0-9]+)')


def on_connect(mosq, obj, rc):
    # set last will and testament
    mosq.will_set(config.MQTT_TOPIC_TESTAMENT, json.dumps({'setavailable': False, 'deviceid': config.DEVICE_ID}), config.MQTT_QOS, retained)

    # register at server
    # registration will be ignored, if already done
    mqttc.publish(config.MQTT_TOPIC_SERVER + '/registration', json.dumps({'function': 'register', 'scope': config.SCOPE, 'deviceid': config.DEVICE_ID}), config.MQTT_QOS, retained)

    # "login" at server > set available true
    mqttc.publish(config.MQTT_TOPIC_SERVER + '/availability', json.dumps({'setavailable': True, 'deviceid': config.DEVICE_ID}), config.MQTT_QOS, retained)

    # initial status update to have correct retained message in statusupdate topic
    send_statusupdate(mqttc)
    # subscribe to topic for incoming requests
    mqttc.subscribe(config.MQTT_TOPIC_REQUESTS, config.MQTT_QOS)

    print("rc: " + str(rc))


def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    matcher = pattern.match(msg.topic)

    source = matcher.group(1)
    target = matcher.group(2)
    issue = matcher.group(3)

    decoded = json.loads(msg.payload.decode('utf-8'))
    function = decoded['function']

    if (target == config.DEVICE_ID):


        if (issue == 'status'):
            if (function == 'setcolor'):
                color = [int(decoded['color'][0]), int(decoded['color'][1]), int(decoded['color'][2])]
                led.setColor(color[0], color[1], color[2])
                send_statusupdate(mosq)
            elif (function == 'getcolor'):
                send_statusupdate(mosq)
            else:
                print('no valid function')
        else:
            print('no valid issue')


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    print(string)


def on_disconnect(mosq, obj, rc):
    print("successfully disconnected")


def signal_handler(signal, frame):
    # "logoff" before disconnect
    mqttc.publish(config.MQTT_TOPIC_SERVER + '/availability', json.dumps({'setavailable': False, 'deviceid': config.DEVICE_ID}), config.MQTT_QOS, retained)

    # unregister; not neccessary
    # mqttc.publish(config.MQTT_TOPIC_SERVER + "/registration", json.dumps({'function': 'unregister', 'deviceid': config.DEVICE_ID}), config.MQTT_QOS, notretained)

    mqttc.disconnect()
    time.sleep(2)
    sys.exit(0)


def send_statusupdate(mosq):
    color = led.getColor()
    mosq.publish(config.MQTT_TOPIC_STATUSUPDATE, json.dumps({'deviceid': config.DEVICE_ID, 'color': color}), config.MQTT_QOS, retained)


# If you want to use a specific client id, use
# mqttc = mosquitto.Mosquitto("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client(config.DEVICE_ID)

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

#mqttc.connect(config.MQTT_HOST, config.MQTT_PORT)
mqttc.connect_async(config.MQTT_HOST, config.MQTT_PORT)

# Uncomment to enable debug messages
#mqttc.on_log = on_log

#mosq.subscribe("$SYS/#", 0)

#mqttc.loop_forever()
mqttc.loop_start()

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to quit')
signal.pause()
