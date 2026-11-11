"""Probe bundled Tk's documented PPM/PGM file reader on valid ASCII controls."""

import json
import sys
import tkinter as tk


def main(paths):
    root = tk.Tk()
    root.withdraw()
    results = []
    for path in paths:
        try:
            image = tk.PhotoImage(file=path, master=root)
            results.append({"path": path, "parsed": True,
                            "width": image.width(), "height": image.height(),
                            "rgb0": list(image.get(0, 0))})
        except tk.TclError as exc:
            results.append({"path": path, "parsed": False, "error": str(exc)})
    version = root.tk.call("info", "patchlevel")
    root.destroy()
    return {"tk_version": version, "controls": results}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: standard.py CONTROL_PATH [...]")
    print(json.dumps(main(sys.argv[1:])))
