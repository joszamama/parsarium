# audioread — WAV / Python

Pinned release: `3.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/audioread/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python audioread
python3 parsarium.py run wav python audioread controls/wav/four-samples.wav
python3 parsarium.py replay wav python audioread CORPUS_DIR runs/wav-audioread-replay
python3 parsarium.py afl build wav python audioread
python3 parsarium.py afl prepare wav python audioread runs/wav-audioread-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
