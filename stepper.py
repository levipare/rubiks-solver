import RPi.GPIO as GPIO
import time
from enum import Enum


class Direction(Enum):
    CW = 1
    CCW = 0


class Motor:
    dir = Direction.CW

    def __init__(self, step_pin: int, dir_pin: int):
        self.step_pin = step_pin
        self.dir_pin = dir_pin

        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)

        self.__set_direction(Direction.CW)

    def __set_direction(self, dir: Direction):
        """
        Sets the direction that the motor will move in
        @param dir an member of the enum `Direction`
        """
        GPIO.output(self.dir_pin, dir)

    def __move(self, n_steps: int):
        """
        Moves the Motor `n_steps`
        @param n_steps the number of steps to move the motor
        """
        for _ in range(n_steps):
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(0.005)
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(0.005)

    def rotate_90(self):
        """
        Rotate 90 degrees clockwise
        """
        if self.dir == Direction.CCW:
            self.__set_direction(Direction.CW)
        self.__move(90)

    def rotate_180(self):
        """
        Rotate 180 degrees
        """
        self.__move(180)

    def rotate_270(self):
        """
        Rotate 270 degrees clockwise by the means of 90 degrees counterclockwise
        """
        if self.dir == Direction.CW:
            self.__set_direction(Direction.CCW)
        self.__move(90)
