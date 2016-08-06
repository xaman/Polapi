#!/usr/bin/python
# -*- coding: UTF-8 -*-

__version__ = '0.0.1'

import os
import time
import shutil
from datetime import datetime
from PIL import Image
from PIL import ImageEnhance
from Adafruit_Thermal import *
from thermal_printer import ThermalPrinter

MAX_WIDTH = 384
DEBUG = True
PICTURE_PATH = "picture.png"


printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

def _main():
    img = Image.open(PICTURE_PATH)
    if (is_horizontal(img)):
        img = rotate(img)
    img = resize(img)
    log('Printing')
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
    log('Rotating')
    rotated = img.rotate(90, expand=True)
    return rotated


def resize(img):
    log('Resizing')
    width = img.size[0]
    height = img.size[1]
    ratio = float(height) / float(width)
    new_height = float(MAX_WIDTH) * ratio
    resized = img.resize((MAX_WIDTH, int(new_height)), Image.ANTIALIAS)
    return resized


def atkinson_dither(img):
    log('Applying Atkinson dithering')
    img = img.convert('L')
    threshold = 128*[0] + 128*[255]
    for y in range(img.size[1]):
        for x in range(img.size[0]):

            old = img.getpixel((x, y))
            new = threshold[old]
            err = (old - new) >> 3 # divide by 8

            img.putpixel((x, y), new)

            for nxy in [(x+1, y), (x+2, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x, y+2)]:
                try:
                    img.putpixel(nxy, img.getpixel(nxy) + err)
                except IndexError:
                    pass
    return img


def convert_to_1bit(img):
    log('Converting to 1 bit')
    return img.convert('1')


def adjust_brightness(img, value):
    log('Setting brightness')
    enhancer = ImageEnhance.Brightness(img)
    result = enhancer.enhance(value)
    return result


def log(message):
    if DEBUG:
        print message

if __name__ == '__main__':
    _main()
