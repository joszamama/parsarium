# thorvg — SVG / C

Pinned release: `1.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/thorvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c thorvg
python3 parsarium.py run svg c thorvg controls/svg/red-green.svg
python3 parsarium.py replay svg c thorvg CORPUS_DIR runs/svg-thorvg-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg c thorvg
python3 parsarium.py afl prepare svg c thorvg runs/svg-thorvg-afl --fandango 100
python3 parsarium.py afl run runs/svg-thorvg-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Sanitizer exception:** ThorVG's pinned source replaces global operator new with malloc. This triggers AddressSanitizer's alloc-dealloc-mismatch check in libFuzzer's own startup vector before input parsing; the image disables only that mismatch check while retaining ASan memory checks and UBSan.
