# @napi-rs/canvas — SVG / JavaScript

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/napi-rs-canvas/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript napi_rs_canvas
python3 parsarium.py run svg javascript napi_rs_canvas controls/svg/red-green.svg
python3 parsarium.py replay svg javascript napi_rs_canvas CORPUS_DIR runs/svg-napi_rs_canvas-replay
python3 parsarium.py afl build svg javascript napi_rs_canvas
python3 parsarium.py afl prepare svg javascript napi_rs_canvas runs/svg-napi_rs_canvas-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
