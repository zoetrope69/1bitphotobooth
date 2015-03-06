#!/usr/bin/env python

from PIL import Image, ImageChops, ImageOps, ImageFilter

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

def dither(f_in, f_out):
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


crop('image.jpg', 'image_cropped.jpg', size=(384, 384), pad=False)
dither('image_cropped.jpg', 'image_dithered.jpg')
