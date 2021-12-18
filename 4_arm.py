#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Servos
# Author      : William
# Date        : 2019/02/23
# import RPi.GPIO as GPIO
import PCF8591 as ADC
import Adafruit_PCA9685
import time


# pwm0_direction = 1
# pwm1_direction = 0
# pwm2_direction = 1
# pwm3_direction = 1
# pwm4_direction = 0

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)



# pwm0_init = 300
# pwm0_max  = 450
# pwm0_min  = 150
# pwm0_pos  = pwm0_init

angle = [90, 90, 90, 90]
speed = 7 # servo rotation speed.
forward = 1
reverse = -1


def setup():
    ADC.setup(0X48)
    # global state


def ctrl_range(raw, max_genout, min_genout):
    if raw > max_genout:
        raw_output = max_genout
    elif raw < min_genout:
        raw_output = min_genout
    else:
        raw_output = raw
    return int(raw_output)

def rotation(ID, direction, speed):
    global angle
    if direction == 1:
        angle[ID] += speed
    else:
        angle[ID] -= speed
    if angle[ID] >= 500:
        angle[ID] = 500
    if angle[ID] <=100:
        angle[ID] = 100
    print(angle[ID])
    pwm.set_pwm(ID, 0, angle[ID])

def move_servo(value):
    if value == 1:          # servo 1
        rotation(0, forward, speed) # (servo_ID, direction, speed)
    elif value == -1:
        rotation(0, reverse, speed)
    elif value == 2:        # servo 2
        rotation(1, forward, speed)
    elif value == -2:
        rotation(1, reverse, speed)
    elif value == 3:        # servo 3
        rotation(2, forward, speed)
    elif value == -3:
        rotation(2, reverse, speed)
    elif value == 4:        # servo 4
        rotation(3, forward, speed)
    elif value == -4:
        rotation(3, reverse, speed)
    else:
        pass
    
def joystick(): #get joystick result
    # state = ['home', 'up', 'down', 'left', 'right']
    value = 0   
    if ADC.read(0) <= 30:   # servo 1
        value = 1 
    elif ADC.read(0) >= 210: 
        value = -1

    if ADC.read(1) <= 30:   # servo 2
        value = 2
    elif ADC.read(1) >= 210: 
        value = -2

    if ADC.read(2) <= 30:   # servo 3
        value = 3
    elif ADC.read(2) >= 210: 
        value = -3 

    if ADC.read(3) <= 30:   # servo 4
        value = 4
    elif ADC.read(3) >= 210: 
        value = -4
    
    return value

def loop():
    mark = 10
    value = joystick()
    move_servo(value)
    if mark != value:
        print(value)
        mark = value
    time.sleep(0.05)

def destroy():
    pass    


if __name__ == '__main__':
    # try:
    setup()
    while True:
        loop()
        # time.sleep(1)
    # except:
    #     destroy()
    # print("quit")

