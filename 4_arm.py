#!/usr/bin/env python3
import RPi.GPIO as GPIO
import PCF8591 as ADC
import Adafruit_PCA9685
import time

L_btn = 11
R_btn = 12

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# pwm_init = 300        90°
# pwm_max  = 500        180° 
# pwm_min  = 100        0°
 
angle = [300, 300, 300, 300]    # The angle of all servos is 90°.
speed = 7 # servo rotation speed.
forward = 1
reverse = -1



mark = None
state_num = None
state_mark = None

def setup():
    ADC.setup(0X48)
    GPIO.setmode(GPIO.BOARD)	# Numbers GPIOs by physical location
    GPIO.setup(L_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Setup button pin as input an pull it up
    GPIO.setup(R_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Setup button pin as input an pull it up
    
    pwm.set_pwm(0, 0, 300)
    pwm.set_pwm(1, 0, 300)
    pwm.set_pwm(2, 0, 300)
    pwm.set_pwm(3, 0, 300)



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
    if ID == None:
        pass
    else:
        if direction == 1:
            angle[ID] += speed
        else:
            angle[ID] -= speed
        if angle[ID] >= 500:
            angle[ID] = 500
        if angle[ID] <=100:
            angle[ID] = 100

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
        rotation(None, reverse, speed)
    
def joystick(): #get joystick result.
    global state_num, state_mark
    state = ['home','L-pressed', 'L-up', 'L-down', 'L-left', 'L-right',\
             'R-home','R-pressed', 'R-up', 'R-down', 'R-left', 'R-right']
    value = None
    if GPIO.input(L_btn) == 0:
        value = 5
        state_num = 1
    elif GPIO.input(R_btn) == 0:
        value = 6
        state_num = 7
    else:
        value = 0
        state_num = 0

    if ADC.read(1) <= 30:  # servo 1
        value = 1 
        state_num = 4
    elif ADC.read(1)>= 210 :   # servo 1
        value = -1
        state_num = 5

    if ADC.read(0) >= 210:   # servo 2
        value = 2
        state_num = 2
    elif ADC.read(0) <= 30: 
        value = -2
        state_num = 3

    if ADC.read(2) <= 30: # servo 3
        value = 3
        state_num = 9
    elif ADC.read(2)>= 210 :   # servo 3
        value = -3 
        state_num = 8

    if ADC.read(3) <= 30:   # servo 4
        value = 4
        state_num = 10
    elif ADC.read(3) >= 210: 
        value = -4
        state_num = 11
    
    if state_mark != state_num: # print state.
        print(state[state_num])
        state_mark = state_num
    return value

def loop():
    global mark
    value = joystick()
    move_servo(value)
    if mark != value:
        # print(value)
        mark = value
    time.sleep(0.05)

def destroy():
    GPIO.cleanup()   


if __name__ == '__main__':
    setup()
    try:
        while True:
            loop()
    except:
        destroy()

