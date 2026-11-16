# @cf-wasm/resvg — SVG / JavaScript

Pinned release: `0.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/cf-wasm-resvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript cf_wasm_resvg
python3 parsarium.py run svg javascript cf_wasm_resvg controls/svg/red-green.svg
python3 parsarium.py replay svg javascript cf_wasm_resvg CORPUS_DIR runs/svg-cf_wasm_resvg-replay
python3 parsarium.py afl build svg javascript cf_wasm_resvg
python3 parsarium.py afl prepare svg javascript cf_wasm_resvg runs/svg-cf_wasm_resvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
