# raylib — WAV / C++

Pinned release: `6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/raylib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp raylib
python3 parsarium.py run wav cpp raylib controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp raylib CORPUS_DIR runs/wav-raylib-replay
python3 parsarium.py afl build wav cpp raylib
python3 parsarium.py afl prepare wav cpp raylib runs/wav-raylib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
