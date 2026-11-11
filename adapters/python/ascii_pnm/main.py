"""Run one pinned Python ASCII PNM reader on a supplied local control."""

import json
import sys
from pathlib import Path


def rgb(width, height, first, second):
    def channel(values):
        values = [float(value) for value in values[:3]]
        if max(values) <= 1:
            values = [value * 255 for value in values]
        return [round(value) for value in values]

    return {"width": int(width), "height": int(height),
            "rgb0": channel(first), "rgb1": channel(second)}


def array_rgb(image):
    return rgb(image.shape[1], image.shape[0], image[0, 0], image[0, 1])


def run(name: str, path: Path):
    if name == "Pillow":
        from PIL import Image
        with Image.open(path) as image:
            image.load()
            return rgb(*image.size, image.getpixel((0, 0)), image.getpixel((1, 0)))
    if name == "opencv-python-headless":
        import cv2
        image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if image is None:
            raise ValueError("OpenCV did not read the PNM")
        return rgb(image.shape[1], image.shape[0], image[0, 0][::-1], image[0, 1][::-1])
    if name == "imageio":
        import imageio.v3 as imageio
        return array_rgb(imageio.imread(path))
    if name == "scikit-image":
        from skimage import io
        return array_rgb(io.imread(path))
    if name == "matplotlib":
        from matplotlib import image
        return array_rgb(image.imread(str(path)))
    if name == "pyvips":
        import pyvips
        image = pyvips.Image.new_from_file(str(path))
        raw = bytes(image.write_to_memory())
        if image.bands != 3:
            raise ValueError(f"expected 3 PNM bands, got {image.bands}")
        return rgb(image.width, image.height, raw[:3], raw[3:6])
    if name == "Wand":
        from wand.image import Image
        with Image(filename=str(path)) as image:
            raw = image.export_pixels(channel_map="RGB")
            return rgb(image.width, image.height, raw[:3], raw[3:6])
    if name == "pygame":
        import pygame
        image = pygame.image.load(str(path))
        return rgb(*image.get_size(), image.get_at((0, 0)), image.get_at((1, 0)))
    if name == "imagesize":
        import imagesize
        width, height = imagesize.get(str(path))
        return {"width": width, "height": height}
    if name == "OpenImageIO":
        import OpenImageIO
        reader = OpenImageIO.ImageInput.open(str(path))
        if reader is None:
            raise ValueError("OpenImageIO did not read the PNM")
        try:
            spec = reader.spec()
            image = reader.read_image()
            return rgb(spec.width, spec.height, image[0, 0], image[0, 1])
        finally:
            reader.close()
    if name == "PyPNM":
        import pypnm
        width, height, depth, maxval, image = pypnm.pnm2list(str(path))
        if depth != 3 or maxval != 255:
            raise ValueError("unexpected PyPNM depth or maxval")
        return rgb(width, height, image[0][0], image[0][1])
    if name == "netpbmfile":
        import netpbmfile
        return array_rgb(netpbmfile.imread(str(path)))
    if name == "netpbm":
        from netpbm import ImgColor
        image = ImgColor(2, 1).from_file(str(path))
        return rgb(len(image[0]), len(image), image[0][0], image[0][1])
    if name == "pgm-reader":
        from pgm_reader import Reader
        reader = Reader()
        image = reader.read_pgm(str(path))
        return {"width": reader.width, "height": reader.height,
                "gray0": int(image[0, 0]), "gray1": int(image[0, 1])}
    if name in {"PySide6", "PyQt6", "PyQt5"}:
        if name == "PySide6":
            from PySide6.QtGui import QImageReader
        elif name == "PyQt6":
            from PyQt6.QtGui import QImageReader
        else:
            from PyQt5.QtGui import QImageReader
        image = QImageReader(str(path)).read()
        if image.isNull():
            raise ValueError("Qt did not read the PNM")
        def pixel(x):
            color = image.pixelColor(x, 0)
            return [color.red(), color.green(), color.blue()]
        return rgb(image.width(), image.height(), pixel(0), pixel(1))
    if name == "mahotas":
        import mahotas
        return array_rgb(mahotas.imread(str(path)))
    if name == "wxPython":
        import wx
        app = wx.App(False)
        image = wx.Image(str(path), wx.BITMAP_TYPE_PNM)
        if not image.IsOk():
            raise ValueError("wxPython did not read the PNM")
        def pixel(x):
            return [image.GetRed(x, 0), image.GetGreen(x, 0), image.GetBlue(x, 0)]
        result = rgb(image.GetWidth(), image.GetHeight(), pixel(0), pixel(1))
        del image, app
        return result
    if name == "napari-netpbmfile":
        from napari_netpbmfile import napari_get_reader
        reader = napari_get_reader(str(path))
        if reader is None:
            raise ValueError("plugin did not select a reader")
        layers = reader(str(path))
        return array_rgb(layers[0][0])
    raise ValueError(f"unknown package: {name}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: main.py PACKAGE CONTROL_PATH")
    print(json.dumps(run(sys.argv[1], Path(sys.argv[2]))))
