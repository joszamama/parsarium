# PyQt5 — ASCII PNM / Python

Pinned PyQt5 release: `5.15.11`; pinned Qt runtime: `5.15.19`. [Manifest](manifest.json) · [verification receipt](verification.json) · [catalog API and parser-family evidence](../../../../catalog/ascii_pnm/python/pyqt5/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python pyqt5
python3 parsarium.py run ascii_pnm python pyqt5 controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python pyqt5 CORPUS_DIR runs/ascii_pnm-pyqt5-replay
python3 parsarium.py afl build ascii_pnm python pyqt5
python3 parsarium.py afl prepare ascii_pnm python pyqt5 runs/ascii_pnm-pyqt5-afl
```

`QImageReader(local path).read()` returns a 2 × 1 image with red `(255, 0, 0)` and green `(0, 255, 0)` pixels for the valid P3 control. Replace `CORPUS_DIR` with a directory of matching PNM files. `afl prepare` creates a seeded run; it does not start a campaign.

**Feedback:** AFL++ QEMU observes native binary edges in the pinned Qt GUI shared library. [The smoke check](binary-feedback/README.md) demonstrates stable and input-sensitive feedback. The wheel does not expose instrumented Qt decoder source, so the receipt reports no Qt source-line coverage or PNM function-level attribution.
