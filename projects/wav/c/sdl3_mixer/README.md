# sdl3_mixer — WAV / C

Pinned release: `3.2.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/sdl3-mixer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c sdl3_mixer
python3 parsarium.py run wav c sdl3_mixer controls/wav/four-samples.wav
python3 parsarium.py replay wav c sdl3_mixer CORPUS_DIR runs/wav-sdl3_mixer-replay
python3 parsarium.py afl build wav c sdl3_mixer
python3 parsarium.py afl prepare wav c sdl3_mixer runs/wav-sdl3_mixer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
