import time
from random import randint

import RPi.GPIO as GPIO
from importlib_resources import files
from PIL import Image
import os
from pathlib import Path
import furpberry.util.img
from furpberry.util.hardware import Display, LightSense, Motor


class Furby:
    def __init__(
        self,
        x_offset: int = 0,
        y_offset: int = 0,
        height: int = 240,
        width: int = 240,
        rotation: int = 90,
        invert: bool = False,
    ) -> None:
        self.eye_height = height
        self.eye_width = width
        self._rotation = rotation
        self.left_eye: Display = Display(0, x_offset, y_offset, height, width, rotation, invert)
        self.right_eye: Display = Display(1, x_offset, y_offset, height, width, rotation, invert)
        self.light_sensor = LightSense()
        self.motor = Motor()

        self.image_dir = files(furpberry.util).joinpath('img')
        self.images: list[str] = sorted(os.listdir(self.image_dir))
        self.starting_image_index: int = -1

    def open_eyes(self, starting_image_index: int) -> None:
        # crop image into two images
        # display left half on left eye
        # display right_eye half on right_eye eye
        self.starting_image_index = starting_image_index if starting_image_index < len(self.images) else 0
        image_original = Image.open(os.path.join(self.image_dir, self.images[starting_image_index]))
        image_resized = image_original.resize((self.eye_width * 2, self.eye_height))
        
        left_crop = image_resized.crop((0, 0, self.eye_width, self.eye_height))
        right_crop = image_resized.crop((0 + self.eye_width, 0, self.eye_width * 2, self.eye_height))

        self.left_eye.open_eye(left_crop)
        self.right_eye.open_eye(right_crop)

    def close_eyes(self) -> None:
        self.left_eye.close_eye()
        self.right_eye.close_eye()

    def roll_eyes(self):
        self.open_eyes(self.starting_image_index)
        self.starting_image_index += 1
        time.sleep(0.1)

    def wake_up_and_dance(self):
        # move motor and
        # cycle through eyeball images
        starting_eyes_index = randint(0, len(self.images) - 1)
        self.motor.start()
        self.open_eyes(starting_eyes_index)
        while self.light_sensor.measure():
            self.roll_eyes()
        self.close_eyes()
        self.motor.stop()


def run_furby():
    furby = Furby()
    try:
        while True:
            if furby.light_sensor.measure():
                furby.wake_up_and_dance()
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run_furby()
