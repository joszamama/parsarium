# raylib — WAV / C

Pinned release: `6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/raylib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c raylib
python3 parsarium.py run wav c raylib controls/wav/four-samples.wav
python3 parsarium.py replay wav c raylib CORPUS_DIR runs/wav-raylib-replay
python3 parsarium.py afl build wav c raylib
python3 parsarium.py afl prepare wav c raylib runs/wav-raylib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
