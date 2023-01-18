#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# GPIO SETUP
sound_port = 22
led_port = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(sound_port, GPIO.IN)
GPIO.setup(led_port, GPIO.OUT)
GPIO.setwarnings(False)


# led on off
def led_switch(status):
    if status:
        GPIO.output(led_port, GPIO.HIGH)
    else:
        GPIO.output(led_port, GPIO.LOW)


def callback(channel):
    value = GPIO.input(channel)
    print("callback event %s" % value)
    led_switch(value)


GPIO.add_event_detect(sound_port, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(sound_port, callback)  # assign function to GPIO PIN, Run function on changsy

# run program forever after starting
# I Use above callbacks to control GPIOs
while True:
    time.sleep(1)
