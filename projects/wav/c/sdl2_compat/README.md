# sdl2-compat — WAV / C

Pinned release: `2.32.74`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/sdl2-compat/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c sdl2_compat
python3 parsarium.py run wav c sdl2_compat controls/wav/four-samples.wav
python3 parsarium.py replay wav c sdl2_compat CORPUS_DIR runs/wav-sdl2_compat-replay
python3 parsarium.py afl build wav c sdl2_compat
python3 parsarium.py afl prepare wav c sdl2_compat runs/wav-sdl2_compat-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
