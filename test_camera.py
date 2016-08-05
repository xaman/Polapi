#!/usr/bin/python
# -*- coding: UTF-8 -*-

import picamera

PICTURE_PATH = 'image.png'


def _main():
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.capture(PICTURE_PATH)


if __name__ == '__main__':
    _main()
