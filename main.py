#!/usr/bin/env python3

import sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

DEBUG = False


def main():
    flags = set()
    args = []

    for arg in sys.argv:
        if arg[0] == "-":
            flags.add(arg)
        else:
            args.append(arg)

    if "--debug" in flags:
        global DEBUG
        DEBUG = True

    [_, src, dest] = args

    src = Path(src).resolve()
    dest = Path(dest).resolve()

    if not src.exists():
        raise Exception("Src doesn't exist")

    if src.samefile(dest):
        raise Exception("Can't overwrite src")

    if src.is_dir():
        if dest.is_file():
            raise Exception(
                "Can't use a file as destination when source is a directory"
            )

        dest.mkdir(parents=True, exist_ok=True)

        for file in src.iterdir():
            print(f"-> {file}")

            if file.is_dir():
                print(f"{file} is a directory")
                continue

            target = dest / file.name
            if target.exists():
                sys.stderr.write(f"Destination {target} already exists\n")
                continue

            try:
                pic = Image.open(file)
                out = apply_border(pic)
                if not DEBUG:
                    out.save(target)
                    print(f"Saved as {target}")
            except Exception as e:
                sys.stderr.write(f"Failed to process {file}:\n\t{e}\n")

    else:
        if dest.is_dir():
            dest = dest / src.name

        if dest.exists():
            raise Exception(f"Destination {dest} already exists")

        dest.parent.mkdir(parents=True, exist_ok=True)

        pic = Image.open(src)
        out = apply_border(pic)
        if not DEBUG:
            out.save(dest)

    return


def apply_border(pic: Image.Image) -> Image.Image:
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

    return out


if __name__ == "__main__":
    main()
