#!/usr/bin/python
# startup for pidioder
__author__ = 'cygairko'

import light
import time

l = light.Led()


l.start()
l.setcolor(255,255,255)
time.sleep(1)

l.setcolor(255,0,0)
time.sleep(1)

l.setcolor(128,0,0)
time.sleep(1)

l.setcolor(0,255,0)
time.sleep(1)

l.setcolor(0,128,0)
time.sleep(1)

l.setcolor(0,0,255)
time.sleep(1)
l.printcolor()

l.setcolor(0,0,128)
time.sleep(1)

l.setcolor(0,255,255)
time.sleep(1)

l.setcolor(255,255,0)
time.sleep(1)

l.setcolor(255,0,255)
time.sleep(1)

l.setcolor(0,0,0)
time.sleep(1)
l.printcolor()

del l