# scipy — WAV / Python

Pinned release: `1.18.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/scipy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python scipy
python3 parsarium.py run wav python scipy controls/wav/four-samples.wav
python3 parsarium.py replay wav python scipy CORPUS_DIR runs/wav-scipy-replay
python3 parsarium.py afl build wav python scipy
python3 parsarium.py afl prepare wav python scipy runs/wav-scipy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
