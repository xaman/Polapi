#!/usr/bin/python
# -*- coding: UTF-8 -*-

__version__ = '0.0.1'

import os
import time
import Image
import shutil
from datetime import datetime
from PIL import ImageEnhance
from Adafruit_Thermal import *
from printer import ThermalPrinter

MAX_WIDTH = 380


def _main():
    # p = ThermalPrinter(heatTime=100, heatInterval=20, heatingDots=7)
    # p.linefeed()
    # img = Image.open("image.png")
    # if (is_horizontal(img)):
    #     img = rotate(img)
    # img = resize(img)
    # img = convert_to_1bit(img)
    # data = list(img.getdata())
    # w, h = img.size
    # p.print_bitmap(data, w, h, False)
    # p.linefeed(3)
    printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
    print_datetime(printer)
    print_image(printer, "image.png")



def print_datetime(printer):
    now = datetime.now()
    text = now.strftime('%Y-%m-%d %H:%M:%S')
    printer.underlineOn()
    printer.println(text)
    printer.underlineOff()
    printer.sleep()
    printer.wake()


def print_image(printer, path):
    img = Image.open(path)
    if (is_horizontal(img)):
        img = rotate(img)
    img = resize(img)
    #img = atkinson_dither(img)
    img = convert_to_1bit(img)
    printer.printImage(img, True)
    printer.feed(2)
    printer.sleep()
    printer.wake()
    printer.setDefault()


def is_horizontal(img):
    width = img.size[0]
    height = img.size[1]
    return width > height


def rotate(img):
    rotated = img.rotate(90, expand=True)
    print 'Rotated'
    return rotated


def resize(img):
    width = img.size[0]
    height = img.size[1]
    ratio = float(height) / float(width)
    new_height = float(MAX_WIDTH) * ratio
    resized = img.resize((MAX_WIDTH, int(new_height)), Image.ANTIALIAS)
    print 'Resized'
    return resized


def atkinson_dither(img):
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
    return img.convert('1')


def adjust_brightness(img, value):
    enhancer = ImageEnhance.Brightness(img)
    result = enhancer.enhance(value)
    print 'Brightness set'
    return result

if __name__ == '__main__':
    _main()
