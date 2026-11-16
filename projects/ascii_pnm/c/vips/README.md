# vips — ASCII PNM / C

Pinned release: `8.18.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/c/vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm c vips
python3 parsarium.py run ascii_pnm c vips controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm c vips CORPUS_DIR runs/ascii_pnm-vips-replay
python3 parsarium.py afl build ascii_pnm c vips
python3 parsarium.py afl prepare ascii_pnm c vips runs/ascii_pnm-vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
