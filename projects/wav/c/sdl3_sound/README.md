# sdl3_sound — WAV / C

Pinned release: `3.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/sdl3-sound/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c sdl3_sound
python3 parsarium.py run wav c sdl3_sound controls/wav/four-samples.wav
python3 parsarium.py replay wav c sdl3_sound CORPUS_DIR runs/wav-sdl3_sound-replay
python3 parsarium.py afl build wav c sdl3_sound
python3 parsarium.py afl prepare wav c sdl3_sound runs/wav-sdl3_sound-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
