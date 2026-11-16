# sdl3_image — SVG / C++

Pinned release: `3.4.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/sdl3-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp sdl3_image
python3 parsarium.py run svg cpp sdl3_image controls/svg/red-green.svg
python3 parsarium.py replay svg cpp sdl3_image CORPUS_DIR runs/svg-sdl3_image-replay
python3 parsarium.py afl build svg cpp sdl3_image
python3 parsarium.py afl prepare svg cpp sdl3_image runs/svg-sdl3_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
