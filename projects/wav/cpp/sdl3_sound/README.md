# sdl3_sound — WAV / C++

Pinned release: `3.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/sdl3-sound/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp sdl3_sound
python3 parsarium.py run wav cpp sdl3_sound controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp sdl3_sound CORPUS_DIR runs/wav-sdl3_sound-replay
python3 parsarium.py afl build wav cpp sdl3_sound
python3 parsarium.py afl prepare wav cpp sdl3_sound runs/wav-sdl3_sound-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
