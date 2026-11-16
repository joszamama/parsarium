# libvips — SVG / C

Pinned release: `8.18.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/libvips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c libvips
python3 parsarium.py run svg c libvips controls/svg/red-green.svg
python3 parsarium.py replay svg c libvips CORPUS_DIR runs/svg-libvips-replay
python3 parsarium.py afl build svg c libvips
python3 parsarium.py afl prepare svg c libvips runs/svg-libvips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
