# leptonica — ASCII PNM / C++

Pinned release: `1.87.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/cpp/leptonica/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp leptonica
python3 parsarium.py run ascii_pnm cpp leptonica controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm cpp leptonica CORPUS_DIR runs/ascii_pnm-leptonica-replay
python3 parsarium.py afl build ascii_pnm cpp leptonica
python3 parsarium.py afl prepare ascii_pnm cpp leptonica runs/ascii_pnm-leptonica-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
