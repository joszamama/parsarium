# audiomath — WAV / Python

Pinned release: `1.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/audiomath/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python audiomath
python3 parsarium.py run wav python audiomath controls/wav/four-samples.wav
python3 parsarium.py replay wav python audiomath CORPUS_DIR runs/wav-audiomath-replay
python3 parsarium.py afl build wav python audiomath
python3 parsarium.py afl prepare wav python audiomath runs/wav-audiomath-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
