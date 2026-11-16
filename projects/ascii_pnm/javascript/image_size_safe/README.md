# image-size-safe — ASCII PNM / JavaScript

Pinned release: `2.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/image-size-safe/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript image_size_safe
python3 parsarium.py run ascii_pnm javascript image_size_safe controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript image_size_safe CORPUS_DIR runs/ascii_pnm-image_size_safe-replay
python3 parsarium.py afl build ascii_pnm javascript image_size_safe
python3 parsarium.py afl prepare ascii_pnm javascript image_size_safe runs/ascii_pnm-image_size_safe-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
