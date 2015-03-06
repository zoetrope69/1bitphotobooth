#!/usr/bin/env python

from PIL import Image, ImageChops, ImageOps, ImageFilter
from thermalprinter import *
import picamera

def takePicture(f_out):

    camera = picamera.PiCamera()

    camera.resolution(384, 384)
    camera.capture(f_out)

    camera.close()

def crop(f_in, f_out, size=(80,80), pad=False):

    image = Image.open(f_in)
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size

    if pad:
        thumb = image.crop( (0, 0, size[0], size[1]) )

        offset_x = max( (size[0] - image_size[0]) / 2, 0 )
        offset_y = max( (size[1] - image_size[1]) / 2, 0 )

        thumb = ImageChops.offset(thumb, offset_x, offset_y)

    else:
        thumb = ImageOps.fit(image, size, Image.ANTIALIAS, (0.5, 0.5))

    thumb.save(f_out)

def process(f_in, f_out):

    image = Image.open(f_in)

    (
    image
        .convert('L')  # greyscale
        .filter(ImageFilter.SHARPEN)  # sharpen
        .filter(ImageFilter.EDGE_ENHANCE)  # enhance edges
        .convert('1')  # 1 bit dither
        .show() # show on screen
        .save(f_out) # save to file
    )

def printPhoto(f_in):

    printer = Adafruit_Thermal('/dev/ttyAMA0', 19200, timeout=5)

    printer.printImage(Image.open(f_in))

def main():

    takePicture('photo.jpg')
    crop('photo.jpg', 'photo_cropped.jpg', size=(384, 384), pad=False)
    process('photo_cropped.jpg', 'photo_processed.jpg')
    printPhoto('photo_processed.jpg')

main()
