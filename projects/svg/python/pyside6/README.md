# PySide6 (SVG / Python)

PySide6 `6.12.0` provides the documented `QSvgRenderer(local path)` API. The pinned Docker harness renders the valid `2 × 1` SVG and reports red and green pixels. A second valid SVG is checked at `4 × 2`.

From the repository root:

```sh
python3 projects/svg/python/pyside6/control.py verify
python3 projects/svg/python/pyside6/control.py run controls/svg/red-green.svg
python3 projects/svg/python/pyside6/control.py run YOUR_LOCAL_SVG_FILE
```

The container uses an offscreen Qt GUI context. The byte-input bridge accepts up to 1 MiB and limits rendered images to 16,777,216 pixels. The Docker control and native QtSvg module hash are recorded in `control-verification.json`.

This path is staged: the prebuilt PySide6 QtSvg module has no verified parser-source coverage or AFL++ feedback. The separate C++ QtSvg project uses matching 6.12.0 source, but its feedback is not attributed to this Python wheel. See `feedback-blocker.json` for the exact limit.

A bounded AFL++ QEMU check on the valid control timed out before the renderer produced a result, so its map is excluded from the evidence.
