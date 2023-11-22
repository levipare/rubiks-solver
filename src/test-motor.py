import time
import RPi.GPIO as GPIO
import stepper

# MOTOR PIN MAPPINGS
# DO NOT CHANGE
STEP = 37
DIR = 35
SLP = 11
RST = 12

GPIO.setmode(GPIO.BOARD)

GPIO.setup(SLP, GPIO.OUT)
GPIO.setup(RST, GPIO.OUT)

motor = stepper.Motor(STEP, DIR)

GPIO.output(SLP, GPIO.HIGH)
GPIO.output(RST, GPIO.HIGH)

time.sleep(2)
motor.rotate_cw()
time.sleep(0.1)
motor.rotate_ccw()
time.sleep(0.1)

GPIO.output(SLP, GPIO.LOW)
