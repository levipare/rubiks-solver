import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

#Each pair is a step followed by a direction
STEP_1 = 31
STEP_2 = 35
STEP_3 = 36

DIR_1 = 33
DIR_2 = 37
DIR_3 = 38

CW = 1
CCW = 0

#Establishing pins
GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(STEP_1, GPIO.OUT)

GPIO.setup(DIR_2, GPIO.OUT)
GPIO.setup(STEP_2, GPIO.OUT)

GPIO.setup(DIR_3, GPIO.OUT)
GPIO.setup(STEP_3, GPIO.OUT)

#Code to turn each motor once clockwise and counter clockwise
GPIO.output(DIR_1, CW)
for x in range(200):
    GPIO.output(STEP_1, GPIO.LOW)
    sleep(.005)
    GPIO.output(STEP_1, GPIO.HIGH)
    sleep(.005)
sleep(1)
GPIO.output(DIR_1, CCW)
for x in range(200):
    GPIO.output(STEP_1, GPIO.LOW)
    sleep(.005)
    GPIO.output(STEP_1, GPIO.HIGH)
    sleep(.005)

GPIO.output(DIR_2, CW)
for x in range(200):
    GPIO.output(STEP_2, GPIO.LOW)
    sleep(.005)
    GPIO.output(STEP_2, GPIO.HIGH)
    sleep(.005)
sleep(1)
GPIO.output(DIR_2, CCW)
for x in range(200):
    GPIO.output(STEP_2, GPIO.LOW)
    sleep(.005)
    GPIO.output(STEP_2, GPIO.HIGH)
    sleep(.005)


GPIO.output(DIR_3, CW)
for x in range(200):
    GPIO.output(STEP_3, GPIO.LOW)
    sleep(.005)
    GPIO.output(STEP_3, GPIO.HIGH)
    sleep(.005)
sleep(1)
GPIO.output(DIR_3, CCW)
for x in range(200):
    GPIO.output(STEP_3, GPIO.LOW)
    sleep(.005)
    GPIO.output(STEP_3, GPIO.HIGH)
    sleep(.005)

GPIO.cleanup()















