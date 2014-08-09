PyDioder
========

Python script to control LED stripe connected to Raspberry Pi GPIO with MQTT messages.

To connect [IKEA DIODER](http://www.ikea.com/de/de/catalog/products/40192361/) to [Raspberry Pi](http://raspberrypi.org) I followed tutorial from [Kristof](http://krizzblog.de/2013/12/the-pidioder/).

Configuration is done in config.py
Set up at least

* MQTT_HOST
* DEVICE_ID (has to be unique for each actuator)
* SERVER_ID (to match servers ID)

Then just execute mqtt.py as follows:
On Raspberry Pi (as root because GPIO connection will not work without)
````
#!bash

sudo python ./mqtt.py
````

or in mockup mode on any machine with Python installed (calling with ````-d <device_id>```` will overwrite ````DEVICE_ID```` in :
````
#!bash

python ./mqtt.py -m
````




Detailed information how to use this will follow soon.
