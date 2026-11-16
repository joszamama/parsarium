# sdl2_image — PNG / C++

Pinned release: `2.8.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/sdl2-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp sdl2_image
python3 parsarium.py run png cpp sdl2_image controls/png/red-green.png
python3 parsarium.py replay png cpp sdl2_image CORPUS_DIR runs/png-sdl2_image-replay
python3 parsarium.py afl build png cpp sdl2_image
python3 parsarium.py afl prepare png cpp sdl2_image runs/png-sdl2_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
