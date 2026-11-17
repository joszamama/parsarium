# thorvg — SVG / C++

Pinned release: `1.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/thorvg/README.md)

The harness calls the native C++ API from the selected adapter: `tvg::Picture::load(local filename)` and `Picture::size`. Fuzz bytes are written to a fresh `.svg` file under `/tmp` so ThorVG's own file loader reads them. Any positive finite size up to 4096 is accepted, including subpixel sizes; the harness renders at the rounded size with a 1-pixel minimum. `controls/svg/red-green.svg` must give 2x1, and the bundled `one-pixel.svg` and `subpixel.svg` must give 1x1.

## Run from the repository root

```sh
python3 parsarium.py build svg cpp thorvg
python3 parsarium.py run svg cpp thorvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp thorvg CORPUS_DIR runs/svg-thorvg-cpp-replay
python3 parsarium.py afl build svg cpp thorvg
python3 parsarium.py afl prepare svg cpp thorvg runs/svg-thorvg-cpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Sanitizer exception:** ThorVG's pinned source replaces global operator new with malloc. This triggers AddressSanitizer's alloc-dealloc-mismatch check in libFuzzer's own startup vector before input parsing; the image disables only that mismatch check while retaining ASan memory checks and UBSan.

The exact control covers 2,509 ThorVG source lines, including 597 lines in its SVG loader. AFL++ reports 2,063 edges on that control. A second valid SVG takes 353 different edge IDs; repeated runs of the exact control produce the same map.
