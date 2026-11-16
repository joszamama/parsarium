"""Run one pinned Python PNG reader on a supplied valid local PNG."""

import json
import sys
from pathlib import Path


def pixels(width, height, first, second):
    def rgba(values):
        values = [float(value) for value in values]
        if max(values) <= 1:
            values = [value * 255 for value in values]
        return [round(value) for value in values[:4]]

    return {"width": int(width), "height": int(height),
            "rgba0": rgba(first), "rgba1": rgba(second)}


def run(name: str, path: Path):
    data = path.read_bytes()
    if name == "Pillow":
        from PIL import Image
        with Image.open(path) as img:
            img.load()
            return pixels(*img.size, img.getpixel((0, 0)), img.getpixel((1, 0)))
    if name == "opencv-python-headless":
        import cv2
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        return pixels(img.shape[1], img.shape[0], img[0, 0][[2, 1, 0, 3]], img[0, 1][[2, 1, 0, 3]])
    if name == "imageio":
        import imageio.v3 as imageio
        img = imageio.imread(path)
        return pixels(img.shape[1], img.shape[0], img[0, 0], img[0, 1])
    if name == "scikit-image":
        from skimage import io
        img = io.imread(path)
        return pixels(img.shape[1], img.shape[0], img[0, 0], img[0, 1])
    if name == "matplotlib":
        from matplotlib import image
        img = image.imread(str(path))
        return pixels(img.shape[1], img.shape[0], img[0, 0], img[0, 1])
    if name == "pypng":
        import png
        width, height, rows, _ = png.Reader(filename=str(path)).asRGBA8()
        row = next(iter(rows))
        return pixels(width, height, row[:4], row[4:8])
    if name == "imagecodecs":
        import imagecodecs
        img = imagecodecs.png_decode(data)
        return pixels(img.shape[1], img.shape[0], img[0, 0], img[0, 1])
    if name == "pyvips":
        import pyvips
        img = pyvips.Image.new_from_file(str(path))
        raw = bytes(img.write_to_memory())
        return pixels(img.width, img.height, raw[:4], raw[4:8])
    if name == "Wand":
        from wand.image import Image
        with Image(filename=str(path)) as img:
            raw = img.export_pixels(channel_map="RGBA")
            return pixels(img.width, img.height, raw[:4], raw[4:8])
    if name == "Willow":
        from willow.image import Image
        with path.open("rb") as stream:
            width, height = Image.open(stream).get_size()
        return {"width": width, "height": height}
    if name == "pycairo":
        import cairo
        img = cairo.ImageSurface.create_from_png(str(path))
        raw = bytes(img.get_data())
        first = [raw[2], raw[1], raw[0], raw[3]]
        second = [raw[6], raw[5], raw[4], raw[7]]
        return pixels(img.get_width(), img.get_height(), first, second)
    if name == "pygame":
        import pygame
        img = pygame.image.load(str(path))
        return pixels(*img.get_size(), img.get_at((0, 0)), img.get_at((1, 0)))
    if name == "rasterio":
        import rasterio
        with rasterio.open(path) as img:
            raw = img.read()
            return pixels(img.width, img.height, raw[:, 0, 0], raw[:, 0, 1])
    if name == "imagesize":
        import imagesize
        width, height = imagesize.get(str(path))
        return {"width": width, "height": height}
    if name == "apng":
        from apng import PNG
        img = PNG.open(str(path))
        return {"width": img.width, "height": img.height,
                "chunks": [chunk.type for chunk in img.chunks]}
    if name == "pngtools":
        from pngtools import get_type_of_chunk, read_file
        chunks = read_file(str(path))
        return {"chunks": [get_type_of_chunk(chunk).decode("ascii") for chunk in chunks]}
    if name == "imgio":
        import imgio
        img, _ = imgio.imread(path)
        return pixels(img.shape[1], img.shape[0], img[0, 0], img[0, 1])
    if name == "simpleimageio":
        import simpleimageio
        img = simpleimageio.read(str(path))
        return pixels(img.shape[1], img.shape[0], img[0, 0], img[0, 1])
    if name == "OpenImageIO":
        import OpenImageIO
        reader = OpenImageIO.ImageInput.open(str(path))
        if reader is None:
            raise ValueError("OpenImageIO did not open the PNG")
        try:
            spec = reader.spec()
            img = reader.read_image()
            return pixels(spec.width, spec.height, img[0, 0], img[0, 1])
        finally:
            reader.close()
    if name == "pngmeta":
        from pngmeta import PngMeta
        return {"title": PngMeta(path).get("Title")}
    if name == "byteparse":
        from byteparse.formats import PNGFile
        png = PNGFile.parse(data)
        return {"width": png.ihdr.width, "height": png.ihdr.height}
    raise ValueError(f"unknown package: {name}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: main.py PACKAGE CONTROL_PATH")
    print(json.dumps(run(sys.argv[1], Path(sys.argv[2]))))
