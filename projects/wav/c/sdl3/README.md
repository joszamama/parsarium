# sdl3 — WAV / C

Pinned release: `3.4.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/sdl3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c sdl3
python3 parsarium.py run wav c sdl3 controls/wav/four-samples.wav
python3 parsarium.py replay wav c sdl3 CORPUS_DIR runs/wav-sdl3-replay
python3 parsarium.py afl build wav c sdl3
python3 parsarium.py afl prepare wav c sdl3 runs/wav-sdl3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
