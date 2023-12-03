import atexit
import time
import RPi.GPIO as GPIO
from enum import Enum

STEPS_PER_REV = 200
SECONDS = 60

class Direction(Enum):
    CCW = 0 
    CW = 1


class Motor:
    def __init__(self, step_pin: int, dir_pin: int, enable_pin: int, rpm: int = 400):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.set_rpm(rpm)
        
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)

        GPIO.output(self.enable_pin, GPIO.HIGH)
        
        atexit.register(GPIO.output, self.enable_pin, GPIO.HIGH)

        self.__set_direction(Direction.CW)

    def __set_direction(self, dir: Direction):
        """
        Sets the direction that the motor will move in
        @param dir a member of the enum `Direction`
        """
        self.dir = dir
        GPIO.output(self.dir_pin, dir.value)
        time.sleep(0.01)

    def __step_delay(self):
        """
        Sleeps for a specific amount time to maintain the specified RPM 
        """
        time.sleep((SECONDS / STEPS_PER_REV) / self.rpm)
    
    def __move(self, n_steps: int):
        """
        Moves the Motor `n_steps`
        @param n_steps the number of steps to move the motor
        """
        # Enable Motor
        GPIO.output(self.enable_pin, GPIO.LOW)
        for _ in range(n_steps):
            GPIO.output(self.step_pin, GPIO.LOW)
            self.__step_delay()
            GPIO.output(self.step_pin, GPIO.HIGH)
            self.__step_delay()
	# Disable Motor
        GPIO.output(self.enable_pin, GPIO.HIGH)

    def set_rpm(self, rpm: int):
        """
        Set the speed of the motor in RPM (rotations per minute)
        @param rpm the desired # of rotations per minute 
        """
        self.rpm = min(1000, max(1, rpm)) # clamp between 1 and 1000

    def rotate_cw(self):
        """
        Rotate 90 degrees clockwise
        """
        if self.dir != Direction.CW:
            self.__set_direction(Direction.CW)
        self.__move(50)


    def rotate_ccw(self):
        """
        Rotate 90 degrees counterclockwise
	    """
        if self.dir != Direction.CCW:
            self.__set_direction(Direction.CCW)
        self.__move(50)
    
    def rotate_180(self):
        """
        Rotate 180 degrees
        """
        self.__move(100)
