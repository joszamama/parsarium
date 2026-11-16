"""Read a local PNG with Tk PhotoImage and emit parsed dimensions and colors."""

import json
from pathlib import Path
import sys
import tkinter


def parse(path: str) -> dict:
    root = tkinter.Tk()
    root.withdraw()
    try:
        image = tkinter.PhotoImage(file=path, master=root)
        width, height = image.width(), image.height()
        return {
            "width": width,
            "height": height,
            "rgb0": list(image.get(0, 0)) if width and height else None,
            "rgb1": list(image.get(1, 0)) if width > 1 and height else None,
        }
    finally:
        root.destroy()


if __name__ == "__main__":
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_file():
        raise SystemExit("usage: replay.py LOCAL_PNG_FILE")
    print(json.dumps(parse(sys.argv[1])))
