# PyQt6 — SVG / Python

PyQt6 `6.12.0` and Qt `6.12.0` are pinned in the [manifest](manifest.json). The Docker control is verified, while parser-source coverage and native AFL++ feedback are unavailable. See the [control receipt](control-verification.json), [feedback blocker](feedback-blocker.json), and [catalog API evidence](../../../../catalog/svg/python/pyqt6/README.md).

From the repository root:

```sh
python3 projects/svg/python/pyqt6/control.py verify
python3 projects/svg/python/pyqt6/control.py run controls/svg/red-green.svg
python3 projects/svg/python/pyqt6/control.py run YOUR_LOCAL_SVG_FILE
```

`QSvgRenderer(local path)` parses and renders the 2 × 1 control as red `(255, 0, 0, 255)` and green `(0, 255, 0, 255)` pixels. The second valid SVG control renders at 4 × 2. The runner builds the pinned image and accepts a local SVG path. It uses an offscreen Qt GUI context.

AFL++ QEMU and Frida terminated while loading a valid SVG on the tested amd64 and arm64 images, so no parser feedback map is accepted. Python binding lines in the receipt are separate from QtSvg parser coverage. This path is staged and has no verified AFL++ campaign overlay.
