#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    value = GPIO.input(channel)
    print("callback event %s" % value)

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on changsy

# infinite loop
while True:
        time.sleep(1)
