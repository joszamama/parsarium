# PyQt6 — SVG / Python

Pinned release: `6.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/pyqt6/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python pyqt6
python3 parsarium.py run svg python pyqt6 controls/svg/red-green.svg
python3 parsarium.py replay svg python pyqt6 CORPUS_DIR runs/svg-pyqt6-replay
python3 parsarium.py afl build svg python pyqt6
python3 parsarium.py afl prepare svg python pyqt6 runs/svg-pyqt6-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.

**Native parser build:** The pinned wheels are installed unchanged except `libQt6Svg.so.6`, which is replaced by QtSvg 6.12.0 built from its pinned source tarball with LLVM source coverage. Coverage and AFL++ feedback come from that library's `src/svg` sources, which the PyQt6 and PySide6 paths share.
