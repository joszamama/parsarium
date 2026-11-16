# sdl3 — PNG / C++

Pinned release: `3.4.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/sdl3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp sdl3
python3 parsarium.py run png cpp sdl3 controls/png/red-green.png
python3 parsarium.py replay png cpp sdl3 CORPUS_DIR runs/png-sdl3-replay
python3 parsarium.py afl build png cpp sdl3
python3 parsarium.py afl prepare png cpp sdl3 runs/png-sdl3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
