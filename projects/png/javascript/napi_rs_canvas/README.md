# @napi-rs/canvas — PNG / JavaScript

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/napi-rs-canvas/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript napi_rs_canvas
python3 parsarium.py run png javascript napi_rs_canvas controls/png/red-green.png
python3 parsarium.py replay png javascript napi_rs_canvas CORPUS_DIR runs/png-napi_rs_canvas-replay
python3 parsarium.py afl build png javascript napi_rs_canvas
python3 parsarium.py afl prepare png javascript napi_rs_canvas runs/png-napi_rs_canvas-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
