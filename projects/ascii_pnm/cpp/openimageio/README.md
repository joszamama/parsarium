# openimageio — ASCII PNM / C++

Pinned release: `3.2.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/cpp/openimageio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp openimageio
python3 parsarium.py run ascii_pnm cpp openimageio controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm cpp openimageio CORPUS_DIR runs/ascii_pnm-openimageio-replay
python3 parsarium.py afl build ascii_pnm cpp openimageio
python3 parsarium.py afl prepare ascii_pnm cpp openimageio runs/ascii_pnm-openimageio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
