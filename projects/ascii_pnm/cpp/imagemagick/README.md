# imagemagick — ASCII PNM / C++

Pinned release: `7.1.2-35`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/cpp/imagemagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp imagemagick
python3 parsarium.py run ascii_pnm cpp imagemagick controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm cpp imagemagick CORPUS_DIR runs/ascii_pnm-imagemagick-replay
python3 parsarium.py afl build ascii_pnm cpp imagemagick
python3 parsarium.py afl prepare ascii_pnm cpp imagemagick runs/ascii_pnm-imagemagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
