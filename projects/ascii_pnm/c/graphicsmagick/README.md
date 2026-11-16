# graphicsmagick — ASCII PNM / C

Pinned release: `1.3.49`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/c/graphicsmagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm c graphicsmagick
python3 parsarium.py run ascii_pnm c graphicsmagick controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm c graphicsmagick CORPUS_DIR runs/ascii_pnm-graphicsmagick-replay
python3 parsarium.py afl build ascii_pnm c graphicsmagick
python3 parsarium.py afl prepare ascii_pnm c graphicsmagick runs/ascii_pnm-graphicsmagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
