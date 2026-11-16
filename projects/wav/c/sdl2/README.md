# sdl2 — WAV / C

Pinned release: `2.32.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/sdl2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c sdl2
python3 parsarium.py run wav c sdl2 controls/wav/four-samples.wav
python3 parsarium.py replay wav c sdl2 CORPUS_DIR runs/wav-sdl2-replay
python3 parsarium.py afl build wav c sdl2
python3 parsarium.py afl prepare wav c sdl2 runs/wav-sdl2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
