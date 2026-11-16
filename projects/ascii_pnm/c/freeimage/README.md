# freeimage — ASCII PNM / C

Pinned release: `3.18.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/c/freeimage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm c freeimage
python3 parsarium.py run ascii_pnm c freeimage controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm c freeimage CORPUS_DIR runs/ascii_pnm-freeimage-replay
python3 parsarium.py afl build ascii_pnm c freeimage
python3 parsarium.py afl prepare ascii_pnm c freeimage runs/ascii_pnm-freeimage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
