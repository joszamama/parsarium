# thorvg — SVG / C++

Pinned release: `1.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/thorvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp thorvg
python3 parsarium.py run svg cpp thorvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp thorvg CORPUS_DIR runs/svg-thorvg-replay
python3 parsarium.py afl build svg cpp thorvg
python3 parsarium.py afl prepare svg cpp thorvg runs/svg-thorvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Sanitizer exception:** ThorVG's pinned source replaces global operator new with malloc. This triggers AddressSanitizer's alloc-dealloc-mismatch check in libFuzzer's own startup vector before input parsing; the image disables only that mismatch check while retaining ASan memory checks and UBSan.
