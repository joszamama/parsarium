# sdl3_image — PNG / C++

Pinned release: `3.4.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/sdl3-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp sdl3_image
python3 parsarium.py run png cpp sdl3_image controls/png/red-green.png
python3 parsarium.py replay png cpp sdl3_image CORPUS_DIR runs/png-sdl3_image-replay
python3 parsarium.py afl build png cpp sdl3_image
python3 parsarium.py afl prepare png cpp sdl3_image runs/png-sdl3_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
