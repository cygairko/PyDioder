#!/usr/bin/python
# class for mqtt connection
__author__ = 'cygairko'

import json
import signal
import sys
import time
import argparse
import os

import config
import colorlight


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--deviceid', help='provide device Id', default=config.DEVICE_ID, nargs='?')
parser.add_argument('-m', '--mockup', help='starts in mockup mode w/o lights necessary', action='store_true')
args = parser.parse_args()

if args.deviceid:
    print('deviceid =', args.deviceid)

try:
    import paho.mqtt.client as mqtt
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.client"
    import inspect

    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt

led = colorlight.Led(args.mockup)
led.start()

retained = True
notretained = False


def on_connect(mosq, obj, rc):
    # set last will and testament
    # mosq.will_set(config.MQTT_TOPIC_TESTAMENT, json.dumps({'setavailable': False, 'deviceid': args.deviceid, 'last': 'will'}), config.MQTT_QOS, retained)

    # register at server
    # registration will be ignored, if already done
    mqttc.publish(config.MQTT_TOPIC_SERVER + '/registration', get_device_info_json('register'), config.MQTT_QOS, retained)

    # "login" at server > set available true
    mqttc.publish(config.MQTT_TOPIC_SERVER + '/availability', json.dumps({'available': True, 'deviceid': args.deviceid}), config.MQTT_QOS, retained)

    # initial status update to have correct retained message in statusupdate topic
    send_statusupdate(mqttc)
    # subscribe to topic for incoming requests
    mqttc.subscribe(config.MQTT_TOPIC_BASE + '/' + args.deviceid + '/+', config.MQTT_QOS)

    print("rc: " + str(rc))


def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    splittopic = msg.topic.split('/')
    print(splittopic)

    target = splittopic[1]
    issue = splittopic[2]

    decoded = json.loads(msg.payload.decode('utf-8'))
    function = decoded['function']

    if target == args.deviceid:
        if issue == 'status':
            if function == 'setcolor':
                color = [int(decoded['color'][0]), int(decoded['color'][1]), int(decoded['color'][2])]
                led.setColor(color[0], color[1], color[2])
                send_statusupdate(mosq)
                print('set ' + str(led.getColor()))
            elif function == 'getcolor':
                send_statusupdate(mosq)
            elif function == 'switch':
                led.setOn(decoded['state'])
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
    mqttc.publish(config.MQTT_TOPIC_SERVER + '/availability', json.dumps({'available': False, 'deviceid': args.deviceid}), config.MQTT_QOS, retained)

    # unregister; not neccessary
    # just using available true/false
    # mqttc.publish(config.MQTT_TOPIC_SERVER + "/registration", json.dumps({'function': 'unregister', 'deviceid': args.deviceid}), config.MQTT_QOS, notretained)

    mqttc.disconnect()
    time.sleep(2)
    sys.exit(0)


def send_statusupdate(mosq):
    mosq.publish(config.MQTT_TOPIC_STATUSUPDATE, get_device_info_json('update'), config.MQTT_QOS, retained)


def get_device_info_json(function):
    return json.dumps({'function': function, 'deviceid': args.deviceid, 'state': led.isOn(), 'color': led.getColor(), 'scope': config.SCOPE})

# If you want to use a specific client id, use
# mqttc = mosquitto.Mosquitto("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client(args.deviceid)

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

# mqttc.connect(config.MQTT_HOST, config.MQTT_PORT)
mqttc.connect_async(config.MQTT_HOST, config.MQTT_PORT)

# Uncomment to enable debug messages
# mqttc.on_log = on_log

#mosq.subscribe("$SYS/#", 0)

#mqttc.loop_forever()
mqttc.loop_start()

# set last will and testament to let the others know, when client disappears
mqttc.will_set(config.MQTT_TOPIC_TESTAMENT, json.dumps({'available': False, 'deviceid': args.deviceid, 'last': 'will'}), config.MQTT_QOS, retained)

print('Press Ctrl+C to quit')
if sys.platform == 'linux':
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
else:
    os.system("pause")
