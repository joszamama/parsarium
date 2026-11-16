# av — WAV / Python

Pinned release: `19.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/av/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python av
python3 parsarium.py run wav python av controls/wav/four-samples.wav
python3 parsarium.py replay wav python av CORPUS_DIR runs/wav-av-replay
python3 parsarium.py afl build wav python av
python3 parsarium.py afl prepare wav python av runs/wav-av-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
