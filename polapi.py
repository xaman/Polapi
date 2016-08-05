#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import picamera
from PIL import Image
from PIL import ImageEnhance
from Adafruit_Thermal import *
import time
from datetime import datetime

DEBUG = True
PICTURE_PATH = "picture.png"
GPIO_PIN = 23
MAX_WIDTH = 384

working = False
printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)


def main():
    setup_button()
    init_loop()


def setup_button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def init_loop():
    global working
    while True:
        input_state = GPIO.input(GPIO_PIN)
        if input_state == False:
            log('Button pressed!')
            if not working:
                working = True
                take_picture()
                print_datetime()
                print_picture()
                working = False


def take_picture():
    camera = picamera.PiCamera()
    camera.capture(PICTURE_PATH)
    camera.close()
    log('Picture taken!')


def print_datetime():
    now = datetime.now()
    text = now.strftime('%Y-%m-%d %H:%M:%S')
    printer.underlineOn()
    printer.println(text)
    printer.underlineOff()


def print_picture():
    img = Image.open(PICTURE_PATH)
    if (is_horizontal(img)):
        img = rotate(img)
    img = resize(img)
    img = adjust_brightness(img, 1.25)
    log('Printing!')
    printer.printImage(img, True)
    printer.feed(2)
    printer.sleep()	  # Tell printer to sleep
    printer.wake()	   # Call wake() before printing again, even if reset
    printer.setDefault()  # Restore printer to defaults


def is_horizontal(img):
    width = img.size[0]
    height = img.size[1]
    return width > height


def rotate(img):
    rotated = img.rotate(90, expand=True)
    log('Rotated!')
    return rotated


def resize(img):
    width = img.size[0]
    height = img.size[1]
    ratio = float(height) / float(width)
    new_height = float(MAX_WIDTH) * ratio
    resized = img.resize((MAX_WIDTH, int(new_height)), Image.ANTIALIAS)
    log('Resized!')
    return resized


def adjust_brightness(img, value):
    enhancer = ImageEnhance.Brightness(img)
    result = enhancer.enhance(value)
    log('Brightness set!')
    return result


def log(message):
    if (DEBUG):
        print message

if __name__ == '__main__':
    main()
