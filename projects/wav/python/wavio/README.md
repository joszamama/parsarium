# wavio — WAV / Python

Pinned release: `0.0.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/wavio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python wavio
python3 parsarium.py run wav python wavio controls/wav/four-samples.wav
python3 parsarium.py replay wav python wavio CORPUS_DIR runs/wav-wavio-replay
python3 parsarium.py afl build wav python wavio
python3 parsarium.py afl prepare wav python wavio runs/wav-wavio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
