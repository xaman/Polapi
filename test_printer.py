#!/usr/bin/python
# -*- coding: UTF-8 -*-

__version__ = '0.0.1'

import sys
import os
import time
import shutil
from datetime import datetime
from PIL import Image
from PIL import ImageEnhance
from thermal_printer import ThermalPrinter

INPUT = 'picture.png'
OUTPUT = 'output.png'
MAX_WIDTH = 384
DEBUG = True

# Default: heatTime=80, heatInterval=2, heatingDots=7
HEAT_TIME = 140
HEAT_INTERVAL = 2
HEATING_DOTS = 7


def _main():
    path = get_path()
    img = Image.open(path)
    if (is_horizontal(img)):
        img = rotate(img)
    img = resize(img)
    img = convert_to_1bit(img)
    img.save(OUTPUT)
    print_picture(img)


def get_path():
    path = INPUT
    if (len(sys.argv) > 1):
        path = sys.argv[1]
    return path


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
    #return img.convert(mode='1', dither=Image.NONE)
    log('Converting to 1 bit')
    return img.convert('1')


def adjust_brightness(img, value):
    log('Setting brightness')
    enhancer = ImageEnhance.Brightness(img)
    result = enhancer.enhance(value)
    return result


def print_config(printer):
    config = "heatTime=%s, heatInterval=%s, heatingDots=%s" % (HEAT_TIME, HEAT_INTERVAL, HEATING_DOTS)
    printer.print_text(config)
    printer.linefeed()


def print_picture(img):
    data = list(img.getdata())
    w, h = img.size
    printer = ThermalPrinter(heatTime=HEAT_TIME, heatInterval=HEAT_INTERVAL, heatingDots=HEATING_DOTS)
    printer.linefeed()
    printer.print_bitmap(data, w, h, False)
    printer.linefeed(3)


def log(message):
    if DEBUG:
        print message


if __name__ == '__main__':
    _main()
