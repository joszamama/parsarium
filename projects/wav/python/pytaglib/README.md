# pytaglib — WAV / Python

Pinned release: `3.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/pytaglib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python pytaglib
python3 parsarium.py run wav python pytaglib controls/wav/four-samples.wav
python3 parsarium.py replay wav python pytaglib CORPUS_DIR runs/wav-pytaglib-replay
python3 parsarium.py afl build wav python pytaglib
python3 parsarium.py afl prepare wav python pytaglib runs/wav-pytaglib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
