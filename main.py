#!/usr/bin/env python3

import sys
from os import path
from PIL import Image, ImageFilter, ImageEnhance

DEBUG = False
# DEBUG = True


def main():
    [_, src, dest] = sys.argv

    src = path.abspath(src)
    dest = path.abspath(dest)

    if src == dest:
        raise Exception("cannot overwrite src")

    pic = Image.open(src)

    sz = max(pic.size)
    bg = pic.resize((sz, sz))
    if DEBUG:
        bg.show()

    bg = bg.filter(ImageFilter.GaussianBlur(sz / 10))
    if DEBUG:
        bg.show()

    bg = ImageEnhance.Brightness(bg).enhance(0.15)
    if DEBUG:
        bg.show()

    # Background is ok, now copy the image in the center
    target = ((sz - pic.size[0]) // 2, (sz - pic.size[1]) // 2)
    out = bg.copy()
    out.paste(pic, target)
    if DEBUG:
        out.show()

    if not DEBUG:
        out.save(dest)
    return


if __name__ == "__main__":
    main()
