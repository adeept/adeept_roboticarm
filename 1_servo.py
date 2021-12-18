#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Servos

import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


init = 300
max  = 500  # 180 degree.
min  = 100  # 0 degree.

def clean_all():
    global pwm
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(50)
    pwm.set_all_pwm(0, 0)


if __name__ == '__main__':
    while True:
        pwm.set_pwm(0, 0, 100)
        time.sleep(1)
        pwm.set_pwm(0, 0, 500)
        time.sleep(1)

