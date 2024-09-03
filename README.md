# Paige's Absolutely Unhinged Furby Hack Project
This uses a 2012 Furby purchased on ebay and deconstructed. 
It also uses a Raspberry Pi Zero W, a Google Home mini, and ... (TBD)

> You've created something that will wake up and dance when LEDs light up but isn't any more useful than a device that googles things for you? So you've created a Burning Man attendee.
>
>_-- My brother, inspired by (but improved upon) https://xkcd.com/948/_

# Parts and Resources:
- [Inspiration](https://medium.com/@jamesfuthey/furlexa-building-an-animatronic-voice-assistant-the-easy-way-e5b3c8fecbf7)
- [2012 Furby](https://64.media.tumblr.com/cf58d9c6c6fadb70b6f1ff192881edbc/tumblr_inline_oqafps9hnA1uj2r2y_1280.pnj)
  - Eye LED/LCD module removed
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
  - [ST7789 python library](https://github.com/solinnovay/Python_ST7789/tree/master)
  - Used replacement eyes since the alternative was more complex
  - [Forum post for using multiple ST7789's](https://forums.adafruit.com/viewtopic.php?t=183537)
  - [Not sure if this will come in handy](https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/overview)
  - [BMP images of all the different eyes](https://github.com/mncoppola/Furby-2012/tree/master/mask_rom/imgs) from [Code from RECon June 2014](https://github.com/mncoppola/Furby-2012) from [Reverse Engineering a Furby](https://poppopret.org/2013/12/18/reverse-engineering-a-furby/)   

# Extremely Helfpul Resources
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) (Specific guides linked above)

# Some resources I haven't used but might need later
- [Furby source code](https://github.com/iafan/Hacksby)
- [Pyfurby](https://github.com/matteoferla/pyfurby) 

