"""Parse a local PNG through the CPython-bundled Tkinter/Tk PhotoImage API."""

import json
import sys
import tkinter


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: standard.py CONTROL_PATH")
    root = tkinter.Tk()
    try:
        root.withdraw()
        image = tkinter.PhotoImage(file=sys.argv[1], master=root)
        print(json.dumps({"width": image.width(), "height": image.height(),
                          "rgb0": list(image.get(0, 0)),
                          "rgb1": list(image.get(1, 0))}))
    finally:
        root.destroy()


if __name__ == "__main__":
    main()
