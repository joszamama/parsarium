# @napi-rs/image — ASCII PNM / JavaScript

Pinned release: `1.16.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/napi-rs-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript napi_rs_image
python3 parsarium.py run ascii_pnm javascript napi_rs_image controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript napi_rs_image CORPUS_DIR runs/ascii_pnm-napi_rs_image-replay
python3 parsarium.py afl build ascii_pnm javascript napi_rs_image
python3 parsarium.py afl prepare ascii_pnm javascript napi_rs_image runs/ascii_pnm-napi_rs_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
