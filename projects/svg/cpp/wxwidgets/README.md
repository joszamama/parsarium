# wxwidgets — SVG / C++

Pinned release: `3.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/wxwidgets/README.md)

The build enables wxWidgets' bundled NanoSVG backend (`wxUSE_NANOSVG=1`, `wxUSE_NANOSVG_EXTERNAL=0`, `wxUSE_LUNASVG=0`). The harness writes each input to a local `.svg` file, loads it with `wxBitmapBundle::FromSVGFile`, renders it at its own size (scaled to fit 256×256 when larger), and reads the pixels back with `ConvertToImage`. Coverage is reported for `src/generic/bmpsvg.cpp` and for the bundled `3rdparty/nanosvg/src/` parser and rasterizer.

The 2 × 1 control covers 102 wxWidgets SVG lines and 615 bundled NanoSVG parser lines. A valid 1 × 1 SVG returns `right_rgb: null`. AFL++ reports 625 control edges; a second valid SVG changes 117 edge IDs.

## Run from the repository root

```sh
python3 parsarium.py build svg cpp wxwidgets
python3 parsarium.py run svg cpp wxwidgets controls/svg/red-green.svg
python3 parsarium.py replay svg cpp wxwidgets CORPUS_DIR runs/svg-wxwidgets-replay
python3 parsarium.py afl build svg cpp wxwidgets
python3 parsarium.py afl prepare svg cpp wxwidgets runs/svg-wxwidgets-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
