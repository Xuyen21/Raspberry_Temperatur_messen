#!/usr/bin/python
import RPi.GPIO as GPIO
import time

LOW_NOISE = 1  # noise below threshold
HIGH_NOISE = 2  # noise above threshold
NO_NOISE = 0
# GPIO SETUP
SOUND_PORT = 22
LED_PORT = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PORT, GPIO.IN)
GPIO.setup(LED_PORT, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.output(LED_PORT, GPIO.LOW)  # turn off leds initially

led_noise_mode = NO_NOISE


# led on off
def led_switch(status):
    global led_noise_mode
    if led_noise_mode == HIGH_NOISE:
        return  # high noise already detected
    elif status == 1:  # high noise detected
        # do the high noise led sequence
        led_noise_mode = HIGH_NOISE
        GPIO.output(LED_PORT, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PORT, GPIO.LOW)
        led_noise_mode = NO_NOISE
    else:
        # noise below threshold
        GPIO.output(LED_PORT, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(LED_PORT, GPIO.LOW)
        time.sleep(0.25)
        GPIO.output(LED_PORT, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(LED_PORT, GPIO.LOW)
        led_noise_mode = NO_NOISE


def callback(channel):
    value = GPIO.input(channel)
    print("callback event %s" % value)
    led_switch(value)


GPIO.add_event_detect(SOUND_PORT, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(SOUND_PORT, callback)  # assign function to GPIO PIN, Run function on changsy

# run program forever after starting
# I Use above callbacks to control GPIOs
while True:
    time.sleep(1)
