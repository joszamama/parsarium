# sdl2_mixer — WAV / C++

Pinned release: `2.8.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/sdl2-mixer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp sdl2_mixer
python3 parsarium.py run wav cpp sdl2_mixer controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp sdl2_mixer CORPUS_DIR runs/wav-sdl2_mixer-replay
python3 parsarium.py afl build wav cpp sdl2_mixer
python3 parsarium.py afl prepare wav cpp sdl2_mixer runs/wav-sdl2_mixer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
