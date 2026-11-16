"""Parse a local valid SVG with one pinned third-party package."""

import json
import sys
from io import BytesIO
from pathlib import Path


def pixels(image):
    rgba = image.convert("RGBA")
    return {"size": [rgba.width, rgba.height],
            "red": list(rgba.getpixel((0, 0))),
            "green": list(rgba.getpixel((1, 0)))}


def png_pixels(data):
    from PIL import Image
    return pixels(Image.open(BytesIO(data)))


def parse(name, path):
    raw = Path(path).read_bytes()
    svg = raw.decode("utf-8")

    if name == "CairoSVG":
        import cairosvg
        return png_pixels(cairosvg.svg2png(bytestring=raw))

    if name == "svglib":
        from svglib.svglib import svg2rlg
        drawing = svg2rlg(str(path))
        return {"size_points": [drawing.width, drawing.height],
                "groups": len(drawing.contents)}

    if name == "svgutils":
        from svgutils.transform import fromfile
        figure = fromfile(str(path))
        return {"size": list(figure.get_size()),
                "elements": len(figure.getroot().root)}

    if name == "svgpathtools":
        from svgpathtools import svg2paths2
        paths, attributes, svg_attributes = svg2paths2(str(path))
        return {"paths": len(paths), "width": svg_attributes["width"],
                "height": svg_attributes["height"],
                "blue_path": next(a["d"] for a in attributes if a.get("fill") == "#0000ff")}

    if name == "resvg_py":
        import resvg_py
        return png_pixels(resvg_py.svg_to_bytes(svg_path=str(path)))

    if name == "svglab":
        from svglab import parse_svg
        root = parse_svg(raw)
        return {"size": [int(root.width.value), int(root.height.value)],
                "fills": [str(shape.fill) for shape in root.children]}

    if name == "svgelements":
        from svgelements import SVG
        root = SVG.parse(str(path))
        return {"size": [int(root.width), int(root.height)],
                "rectangles": sum(type(element).__name__ == "Rect" for element in root.elements())}

    if name == "resvg":
        import resvg
        tree = resvg.usvg.Tree.from_str(svg, resvg.usvg.Options.default())
        return {"size": list(tree.int_size())}

    if name == "mpl-simple-svg-parser":
        from mpl_simple_svg_parser import SVGMplPathIterator
        iterator = SVGMplPathIterator(raw)
        entries = list(iterator.iter_path_attrib())
        return {"viewbox": iterator.parse_viewbox(), "paths": len(entries)}

    if name == "pyvips":
        import pyvips
        image = pyvips.Image.new_from_file(str(path))
        return {"size": [image.width, image.height],
                "red": list(image.getpoint(0, 0)),
                "green": list(image.getpoint(1, 0))}

    if name == "Wand":
        from wand.image import Image
        with Image(filename=str(path)) as image:
            return {"size": [image.width, image.height],
                    "red": [image[0, 0].red_int8, image[0, 0].green_int8,
                            image[0, 0].blue_int8, image[0, 0].alpha_int8],
                    "green": [image[1, 0].red_int8, image[1, 0].green_int8,
                              image[1, 0].blue_int8, image[1, 0].alpha_int8]}

    if name == "scour":
        from scour.scour import scourString
        from lxml import etree
        optimized = scourString(svg)
        root = etree.fromstring(optimized.encode())
        rectangles = root.findall("{http://www.w3.org/2000/svg}rect")
        return {"size": [root.get("width"), root.get("height")],
                "rectangles": len(rectangles),
                "optimized_fills": [rectangle.get("fill") for rectangle in rectangles]}

    if name == "picosvg":
        from picosvg.svg import SVG
        root = SVG.parse(str(path)).svg_root
        return {"size": [root.attrib["width"], root.attrib["height"]],
                "rectangles": len(root.findall("{http://www.w3.org/2000/svg}rect"))}

    if name == "resvglite":
        import resvglite
        return png_pixels(resvglite.render_svg(raw, size_px=1)[0])

    if name == "pillow-lunasvg":
        import pillow_lunasvg
        from PIL import Image
        return pixels(Image.open(str(path)))

    if name == "picosvgx":
        from picosvgx.svg import SVG
        root = SVG.parse(str(path)).svg_root
        return {"size": [root.attrib["width"], root.attrib["height"]],
                "rectangles": len(root.findall("{http://www.w3.org/2000/svg}rect"))}

    if name == "skia-python":
        import skia
        tree = skia.SVGDOM.MakeFromStream(skia.MemoryStream.MakeCopy(raw))
        size = tree.containerSize()
        return {"size": [size.width(), size.height()]}

    if name == "PyMuPDF":
        import pymupdf
        with pymupdf.open(str(path)) as document:
            page = document[0]
            return {"pages": len(document), "size": [page.rect.width, page.rect.height]}

    if name in ("PyQt6", "PySide6"):
        if name == "PyQt6":
            from PyQt6.QtCore import QSize
            from PyQt6.QtGui import QImage, QPainter
            from PyQt6.QtSvg import QSvgRenderer
        else:
            from PySide6.QtCore import QSize
            from PySide6.QtGui import QImage, QPainter
            from PySide6.QtSvg import QSvgRenderer
        renderer = QSvgRenderer(str(path))
        if not renderer.isValid():
            raise ValueError("SVG renderer rejected control")
        size = renderer.defaultSize()
        image = QImage(size, QImage.Format.Format_ARGB32)
        image.fill(0)
        painter = QPainter(image)
        renderer.render(painter)
        painter.end()
        return {"size": [size.width(), size.height()],
                "red": list(image.pixelColor(0, 0).getRgb()),
                "green": list(image.pixelColor(1, 0).getRgb())}

    raise ValueError(f"unknown parser: {name}")


if __name__ == "__main__":
    print(json.dumps(parse(sys.argv[1], Path(sys.argv[2])), sort_keys=True))
