"""Run one pinned Python PNG reader on a supplied valid local PNG."""

import json
import sys
from pathlib import Path


def rgba(value):
    """One decoded pixel as 8-bit RGBA, expanded per PNG convention.

    Gray repeats into r, g and b; a missing alpha is 255; 16-bit samples keep
    their high byte; float samples in 0..1 are scaled by 255.
    """
    dtype = getattr(value, "dtype", None)
    if hasattr(value, "tolist"):
        value = value.tolist()
    values = [value] if isinstance(value, (int, float)) else list(value)
    if dtype is not None and dtype.kind == "u" and dtype.itemsize == 2:
        values = [int(sample) >> 8 for sample in values]
    elif any(isinstance(sample, float) for sample in values):
        values = [float(sample) for sample in values]
        if max(values) <= 1:
            values = [sample * 255 for sample in values]
    if len(values) in (1, 2):
        values = values[:1] * 3 + values[1:]
    if len(values) == 3:
        values = values + [255]
    return [round(sample) for sample in values[:4]]


def pixels(width, height, at):
    """Report the size, pixel (0,0) and, when the image has one, pixel (1,0)."""
    result = {"width": int(width), "height": int(height), "rgba0": rgba(at(0))}
    if int(width) > 1:
        result["rgba1"] = rgba(at(1))
    return result


def run(name: str, path: Path):
    data = path.read_bytes()
    if name == "Pillow":
        from PIL import Image
        with Image.open(path) as img:
            img.load()
            img = img.convert("RGBA")
            return pixels(*img.size, lambda x: img.getpixel((x, 0)))
    if name == "opencv-python-headless":
        import cv2
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("OpenCV did not decode the PNG")

        def at(x):
            pixel = img[0, x]
            if img.ndim == 3 and img.shape[2] >= 3:
                # OpenCV stores color samples as BGR or BGRA.
                pixel = pixel[[2, 1, 0, 3] if img.shape[2] == 4 else [2, 1, 0]]
            return pixel
        return pixels(img.shape[1], img.shape[0], at)
    if name == "imageio":
        import imageio.v3 as imageio
        img = imageio.imread(path)
        return pixels(img.shape[1], img.shape[0], lambda x: img[0, x])
    if name == "scikit-image":
        from skimage import io
        img = io.imread(path)
        return pixels(img.shape[1], img.shape[0], lambda x: img[0, x])
    if name == "matplotlib":
        from matplotlib import image
        img = image.imread(str(path))
        return pixels(img.shape[1], img.shape[0], lambda x: img[0, x])
    if name == "pypng":
        import png
        width, height, rows, _ = png.Reader(filename=str(path)).asRGBA8()
        row = next(iter(rows))
        return pixels(width, height, lambda x: row[4 * x:4 * x + 4])
    if name == "imagecodecs":
        import imagecodecs
        img = imagecodecs.png_decode(data)
        return pixels(img.shape[1], img.shape[0], lambda x: img[0, x])
    if name == "pyvips":
        import pyvips
        img = pyvips.Image.new_from_file(str(path))
        raw = bytes(img.write_to_memory())
        return pixels(img.width, img.height, lambda x: raw[4 * x:4 * x + 4])
    if name == "Wand":
        from wand.image import Image
        with Image(filename=str(path)) as img:
            raw = img.export_pixels(channel_map="RGBA")
            return pixels(img.width, img.height, lambda x: raw[4 * x:4 * x + 4])
    if name == "Willow":
        from willow.image import Image
        with path.open("rb") as stream:
            width, height = Image.open(stream).get_size()
        return {"width": width, "height": height}
    if name == "pycairo":
        import cairo
        import struct
        img = cairo.ImageSurface.create_from_png(str(path))
        raw = bytes(img.get_data())
        image_format = img.get_format()

        def float_byte(value):
            # Cairo stores 16-bit PNG samples as value / 65535; keep the high byte.
            return 0 if not value > 0.0 else 255 if value >= 1.0 else int(value * 65535.0 + 0.5) >> 8

        def at(x):
            # Cairo premultiplies colour by alpha in ARGB32 and RGBA128F; report straight RGBA.
            if image_format in (cairo.Format.RGBA128F, cairo.Format.RGB96F):
                bands = 4 if image_format == cairo.Format.RGBA128F else 3
                values = list(struct.unpack_from(f"={bands}f", raw, x * bands * 4)) + [1.0] * (4 - bands)
                if image_format == cairo.Format.RGBA128F and values[3] > 0.0:
                    values[:3] = [value / values[3] for value in values[:3]]
                return [float_byte(value) for value in values]
            (value,) = struct.unpack_from("=I", raw, x * 4)
            alpha = value >> 24 if image_format == cairo.Format.ARGB32 else 255
            colour = [(value >> shift) & 255 for shift in (16, 8, 0)]
            if alpha not in (0, 255):
                colour = [min(255, (sample * 510 + alpha) // (2 * alpha)) for sample in colour]
            return colour + [alpha]
        return pixels(img.get_width(), img.get_height(), at)
    if name == "pygame":
        import pygame
        img = pygame.image.load(str(path))
        return pixels(*img.get_size(), lambda x: img.get_at((x, 0)))
    if name == "rasterio":
        import rasterio
        with rasterio.open(path) as img:
            raw = img.read()
            colormap = None
            if img.count == 1 and img.colorinterp[0].name == "palette":
                colormap = img.colormap(1)
            # GDAL keeps 1, 2 and 4-bit samples unscaled and reports their depth as NBITS.
            nbits = int(img.tags(1, ns="IMAGE_STRUCTURE").get("NBITS", 8))

            def at(x):
                if colormap is not None:
                    return list(colormap[int(raw[0, 0, x])])
                if nbits < 8:
                    return [int(sample) * 255 // ((1 << nbits) - 1) for sample in raw[:, 0, x]]
                return raw[:, 0, x]
            return pixels(img.width, img.height, at)
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
        return pixels(img.shape[1], img.shape[0], lambda x: img[0, x])
    if name == "simpleimageio":
        import simpleimageio
        img = simpleimageio.read(str(path))
        return pixels(img.shape[1], img.shape[0], lambda x: img[0, x])
    if name == "OpenImageIO":
        import OpenImageIO
        reader = OpenImageIO.ImageInput.open(str(path))
        if reader is None:
            raise ValueError("OpenImageIO did not open the PNG")
        try:
            spec = reader.spec()
            img = reader.read_image()
            return pixels(spec.width, spec.height, lambda x: img[0, x])
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
