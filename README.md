# Paige's Absolutely Unhinged Furby Hack Project
This uses a 2012 Furby purchased on ebay and deconstructed. 
It also uses a Raspberry Pi Zero W, a Google Home mini, solder,
and hot glue.

> You've created something that will wake up and dance when LEDs light up but isn't any more useful than a device that googles things for you? So you've created a Burning Man attendee.
>
>_-- My brother, inspired by (but improved upon) https://xkcd.com/948/_

> Paige can glue any two things together with alarming speed.
>
> _--Anonymous peer_

# Wiring:
The hardware is listed in the section below. This chart shows my wiring, 
using exactly the hardware I selected. If you wish to change the wiring 
in any way, the pins are assigned in /src/furpberry/util/hardware.py.
Since the ST7789 package insisted on using GPIO/BCM numbering and I hate 
that, I have included both in this table. There is an abstraction layer 
in the form of an enum called "Pin" also defined in hardware.py that 
just maps the Pi pin number to its corresponding BCM pin number so when 
I need to verify that the wires are correctly routed, I can just count.

| Pi Pin | GPIO Pin | Peripheral Pin           | Description                                            |
|--------|----------|--------------------------|--------------------------------------------------------|
| 1      | -        | Light sensor Vin         | 3V3 supply voltage for CdS                             |
| 2      | -        | TB6612 VCC               | Motor control 5V supply (VCC) (NOT motor power)        |
| 3      | -        | ST7789 VCC               | Shared peripheral 5V supply (VCC for both displays)    |
| 6      | -        | ST7789 GND               | Shared peripheral GND (display GND, motor control GND) |
| 7      | 4        | TB6612 PWM               | Motor control PWM                                      |
| 11     | 17       | TB6612 AIN2              | Motor control AIN2                                     |
| 12     | 18       | TB6612 AIN1              | Motor control AIN1                                     |
| 18     | 24       | ST7789 RST               | Left display reset bit                                 |
| 19     | 10       | ST7789 SDA               | (SPI0 MOSI) (shared between two displays)              |
| 22     | 25       | ST7789 DC                | (SPI0 MISO) (shared between two displays)              |
| 23     | 11       | ST7789 SCLK              | (SPI0) (shared between two displays)                   |
| 24     | 8        | ST7789 CS                | Right display chip select (SPI0 CE1)                   |
| 26     | 7        | ST7789 CS                | Left display chip select (SPI0 CE0)                    |
| 29     | 5        | ST7789 Backlight         | Backlight control for both displays                    |
| 31     | 6        | ST7789 RST               | Right display reset bit                                |
| 39     | -        | Light sensor GND         |                                                        |
| 40     | 21       | Light sensor measurement |                                                        |

# Parts and Resources:
- [Inspiration](https://medium.com/@jamesfuthey/furlexa-building-an-animatronic-voice-assistant-the-easy-way-e5b3c8fecbf7)
- [2012 Furby](https://64.media.tumblr.com/cf58d9c6c6fadb70b6f1ff192881edbc/tumblr_inline_oqafps9hnA1uj2r2y_1280.pnj)
  - Display LED/LCD module removed
  - Original circuitboard removed
  - Microphone, speaker, battery pack removed
  - Bottom hinges removed to make room for Google Home Mini to be used as a base
- [Raspberry Pi Zero W](https://www.adafruit.com/product/3400#tutorials)
  - [MicroSD card](https://www.adafruit.com/product/1294)
- [TB6612 1.2A DC/Stepper Motor Driver Breakout Board](https://www.adafruit.com/product/2448)
  - [With original Furby motor (6V 500mA DC motor)](https://howchoo.com/pi/controlling-dc-motors-using-your-raspberry-pi/)
  - [With PWM](https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/)
- [Google Home Mini with top removed](https://www.ifixit.com/Teardown/Google+Home+Mini+Teardown/102264?srsltid=AfmBOoo-8CsShgmN08UxHM-caZ9PjHB-rYH-7HNRVJ8b5ZWtjJqI-l1G)
- [CdS Photoresistor](https://www.adafruit.com/product/161) to detect when Google Home is doing stuff
  - [Tutorial](https://learn.adafruit.com/photocells)
  - [RPi forum post about wiring phototransistor](https://forums.raspberrypi.com/viewtopic.php?t=207040)
  - [Configuring the GPIO for an input](https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/)
  - I did use a resistor as indicated but the GPIO is digital and I only need light/no light
- [2 LCD OLED Display Modules (to replace eyes)](https://www.aliexpress.us/item/3256804844327418.html)
  - I got 2 1.54 inch modules but may have been able to use something smaller
  - [Forum post for using multiple ST7789's](https://forums.adafruit.com/viewtopic.php?t=183537)
  - [Python library](https://github.com/pimoroni/st7789-python) - dual displays is broken on versions 1.0.0 and 1.0.1 but 0.0.4 works fine
  - [Not sure if this will come in handy](https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/overview)
  - [BMP images of all the different eyes](https://github.com/mncoppola/Furby-2012/tree/master/mask_rom/imgs) from [Code from RECon June 2014](https://github.com/mncoppola/Furby-2012) from [Reverse Engineering a Furby](https://poppopret.org/2013/12/18/reverse-engineering-a-furby/)

# Usage
From repository root:
```
make venv
source venv/bin/activate
furbalicious
```
This will loop forever (unless it's broken) and will activate the motor and eyes when the light
sensor detects something, and sleep otherwise.

# Future Plans:
[] Include sound input to continue motion if music is playing? Currently, this is light-activated only. 
[] Replace Google home mini with Alexa so I can set my own activation phrase? Low priority but it would be cool to have it respond to "hey furby"
[] Build a second one using my own instructions and update as needed
[] Include startup script (setup and run on powerup)
