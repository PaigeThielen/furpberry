from enum import Enum

import RPi.GPIO as GPIO
import ST7789 as st7789
from PIL import Image

# Declare the GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Pin(Enum):
    """GPIO pin ID from Pi pin ID"""

    PI3 = 2
    PI5 = 7
    PI7 = 4
    PI8 = 14
    PI10 = 15
    PI11 = 17
    PI12 = 18
    PI13 = 27
    PI15 = 22
    PI16 = 23
    PI18 = 24
    PI19 = 10
    PI21 = 9
    PI22 = 25
    PI23 = 11
    PI24 = 8
    PI26 = 7
    PI27 = 0
    PI28 = 1
    PI29 = 5
    PI31 = 6
    PI32 = 12
    PI33 = 13
    PI35 = 19
    PI36 = 16
    PI37 = 26
    PI38 = 20
    PI40 = 21
    CS0 = 0
    CS1 = 1


class Display:
    # Pin mapping for eyes.
    # The st7789 python drivers use BCM numbers and everything else in my repo uses board numbering
    # Because BCM numbering is bonkers and board numbering actually makes sense
    def __init__(
        self,
        spi_id: int,
        x_offset: int = 0,
        y_offset: int = 0,
        height: int = 240,
        width: int = 240,
        rotation: int = 90,
        invert: bool = False,
    ) -> None:
        self.CLK = Pin.PI23.value  # BCM 11
        self.SDA = Pin.PI19.value  # BCM 10
        self.DC = Pin.PI22.value  # BCM 25
        self.BACKLIGHT = Pin.PI29.value
        self._height = height
        self._width = width
        self._rotation = rotation
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._invert = invert

        if spi_id == 0:
            self.RST = Pin.PI18.value
            self.CS = 0
        elif spi_id == 1:
            self.RST = Pin.PI31.value
            self.CS = 1
        else:
            raise ValueError("Invalid SPI ID")

        self.display = st7789.ST7789(
            height=self._height,
            width=self._width,
            rotation=self._rotation,
            port=0,
            cs=self.CS,
            dc=self.DC,
            rst=self.RST,
            backlight=self.BACKLIGHT,
            spi_speed_hz=20 * 1000 * 1000,
            offset_left=self._x_offset,
            offset_top=self._y_offset,
            invert=self._invert,
        )

        self.display.begin()
        self.close_eye()

    def open_eye(self, image: Image) -> None:
        self.display.display(image)
        self.backlight(True)

    def close_eye(self):
        # self.display.clear()
        self.backlight(False)

    def backlight(self, on: bool) -> None:
        self.display.set_backlight(on)


class Motor:
    """
    Pinouts for pi zero W motor control with TB6612.
    Motor is the motor for a 2012 Furby.
    Motor power supply is furby battery pack.
    The motor is Motor A, wired per
    https://howchoo.com/pi/controlling-dc-motors-using-your-raspberry-pi
    """

    def __init__(
        self,
        pwm: Pin = Pin.PI7,
        in1: Pin = Pin.PI12,
        in2: Pin = Pin.PI11,
        standby: Pin = Pin.PI13,
        dutyCycle: float = 25.0,
    ):
        self.pwm = pwm.value
        self.in1 = in1.value
        self.in2 = in2.value
        self.standby = standby.value
        self.dutyCycle = dutyCycle
        self.frequency = 100

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


class LightSense:
    def __init__(self, measurement_pin: Pin = Pin.PI40):
        self.measurement_pin = measurement_pin.value

        # set up GPIO pin for light sensor as input
        GPIO.setup(self.measurement_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def measure(self) -> bool:
        """Returns True if light is detected"""
        return GPIO.input(self.measurement_pin) == GPIO.HIGH

    def wait_for_edge(self, type: GPIO):
        GPIO.wait_for_edge(self.measurement_pin, type)
