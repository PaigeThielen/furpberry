#!/usr/bin/env python

# Import required modules
from time import sleep
#from datetime import timedelta, datetime
from random import randint, random

import RPi.GPIO as GPIO


class Motor:
    """
    Pinouts for pi zero W motor control with TB6612.
    Motor is the motor for a 2012 Furby.
    Motor power supply is furby battery pack.
    The motor is Motor A, wired per
    https://howchoo.com/pi/controlling-dc-motors-using-your-raspberry-pi
    ----------
    STBY = Pin 13 (GPIO #21)

    Motor A:
    PWMA = Pin 7 (GPIO #4)
    AIN2 = Pin 11 (GPIO #17)
    AIN1 = Pin 12 (GPIO #18)
    """

    def __init__(self, pwm: int = 7, in1: int = 12, in2: int = 11, standby: int = 13, dutyCycle: float = 25.0):
        self.sleepy_duty_cycle = dutyCycle / 2
        self.pwm = pwm
        self.in1 = in1
        self.in2 = in2
        self.standby = standby
        self.dutyCycle = dutyCycle * 2
        self.frequency = 100

        self.setup()

    def setup(self):
        # Declare the GPIO settings
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # set up GPIO pins as outputs, initialize to low
        GPIO.setup(self.pwm, GPIO.OUT, initial=GPIO.LOW)  # Connected to PWMA
        GPIO.setup(self.in2, GPIO.OUT, initial=GPIO.LOW)  # Connected to AIN2
        GPIO.setup(self.in1, GPIO.OUT, initial=GPIO.HIGH)  # Connected to AIN1
        GPIO.setup(self.standby, GPIO.OUT, initial=GPIO.LOW)  # Connected to STBY

        # set up PWM
        self.motorPWM = GPIO.PWM(self.pwm, self.frequency)

    def set_duty_cycle(self, dc: float):
        self.dutyCycle = dc
        self.motorPWM.ChangeDutyCycle(dc)

    def start(self):
        self.motorPWM.start(self.dutyCycle)

    def stop(self):
        self.motorPWM.stop()

    def set_clockwise(self):
        # Set the motor direction to clockwise
        GPIO.output(self.in1, GPIO.HIGH)  # Set AIN1
        GPIO.output(self.in2, GPIO.LOW)  # Set AIN2

    def set_counter_clockwise(self):
        # Set the motor direction to counterclockwise
        GPIO.output(self.in1, GPIO.LOW)  # Set AIN1
        GPIO.output(self.in2, GPIO.HIGH)  # Set AIN2

    def set_standby(self):
        # Disable STBY (standby)
        GPIO.output(self.standby, GPIO.HIGH)

    def reset(self):
        # Reset all the GPIO pins by setting them to LOW
        GPIO.output(self.in1, GPIO.LOW)  # Set AIN1
        GPIO.output(self.in2, GPIO.LOW)  # Set AIN2
        GPIO.output(self.pwm, GPIO.LOW)  # Set PWMA
        GPIO.output(self.standby, GPIO.LOW)  # Set STBY

    def wiggle(self, wiggles: int) -> bool:
        self.set_clockwise()
        self.set_standby()
        for iter in range(0, wiggles, 1):
            self.start()
            sleep(randint(3,6))
            self.stop()
            sleep(2 * random())
        self.stop()
        self.set_standby()
