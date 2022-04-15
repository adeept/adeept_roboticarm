#!/usr/bin/env python3
import RPi.GPIO as GPIO
import PCF8591 as ADC
import Adafruit_PCA9685
import time
# import json
# import os



# curpath = os.path.realpath(__file__)
# thisPath = "/" + os.path.dirname(curpath) + "/"

# pwm0_direction = 1
L_btn = 11
R_btn = 12

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)



# pwm_init = 300        90°
# pwm_max  = 500        180° 
# pwm_min  = 100        0°
 
angle = [300, 300, 300, 300]    # The angle of all servos is 90°.
Temporary_angle = [300,300,300,300]
speed = 7 # servo rotation speed.
forward = 1
reverse = -1

servo_angle = []
servo_duration = []
save_memory = 0
ID_change = 0
memory_end = 0


mark = None
ID_mark = None
direction_mark = None
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
    global angle, save_memory, ID_change, Temporary_angle, ID_mark,direction_mark,servo_angle
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
        if save_memory == 1:    # Save the action of the robot arm.
            Temporary_angle = angle
            if ID_mark != ID or direction_mark != direction :   # Change the angle of the servo once and save the data once.
                servo_angle.append([Temporary_angle[0], Temporary_angle[1], Temporary_angle[2], Temporary_angle[3]])
                ID_mark = ID
                direction_mark = direction
                print("-------------------------------")
                print(servo_angle)
                # print(angle)
                print("-------------------------------")
                print('\n')
        print(angle)
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
        state_num = 2
    elif ADC.read(1)>= 210 :   # servo 1
        value = -1
        state_num = 3

    if ADC.read(0) >= 210:   # servo 2
        value = 2
        state_num = 4
    elif ADC.read(0) <= 30: 
        value = -2
        state_num = 5

    if ADC.read(2) <= 30: # servo 3
        value = 3
        state_num = 8
    elif ADC.read(2)>= 210 :   # servo 3
        value = -3 
        state_num = 9

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

# Reduce the rotation speed of the servo between each action.
def memory_angle(ID, speed, target_angle, current_angle):
        buffer_value = target_angle - current_angle
        if abs(buffer_value) <= speed:
            pass
        else:
            direction = None
            while buffer_value != 0:
                if buffer_value < 0:
                    direction = -1
                else:
                    direction = 1
                buffer_value = buffer_value - speed*direction
                pwm.set_pwm(ID, 0, (target_angle - buffer_value))
                if abs(buffer_value) <= speed:
                    break
                time.sleep(0.01) # Action interval time.
            
        time.sleep(0.1)

def play_memory():
    global angle,servo_angle
    target_angle = []
    i = 0
    rotation_speed = 1
    current_angle = angle   # Initial angle.
    for target_angle in servo_angle:    #Read the saved servo angle value.
        print(target_angle)
        memory_angle(0, rotation_speed, target_angle[0], current_angle[0])
        memory_angle(1, rotation_speed, target_angle[1], current_angle[1])
        memory_angle(2, rotation_speed, target_angle[2], current_angle[2])
        memory_angle(3, rotation_speed, target_angle[3], current_angle[3])
        current_angle = target_angle # Update the current servo angle.

def loop():
    global save_memory, mark, memory_end,servo_angle
    play_memory_start = 0
    value = joystick()
    # Save the action function of the robotic arm.
    if save_memory == 0 and value == 5 and memory_end != 1:
        save_memory = 1
        servo_angle = []
        servo_angle.append([angle[0], angle[1], angle[2], angle[3]]) # record initial position.
        print("start!!")
    elif save_memory ==1 and value != 5:
        memory_end = 1
    elif memory_end == 1 and value ==5:
        save_memory = 0
        servo_angle.append([angle[0], angle[1], angle[2], angle[3]]) # record end position.
        print("end!!")
    else:
        memory_end = 0
    # Read memory action.
    if memory_end == 0 and value == 6:
        # Press the button once to execute the saved action \
        # of the robotic arm only once.
        play_memory()

    move_servo(value)
    if mark != value:
        print(value)
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

