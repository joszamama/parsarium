# pydub — WAV / Python

Pinned release: `0.25.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/pydub/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python pydub
python3 parsarium.py run wav python pydub controls/wav/four-samples.wav
python3 parsarium.py replay wav python pydub CORPUS_DIR runs/wav-pydub-replay
python3 parsarium.py afl build wav python pydub
python3 parsarium.py afl prepare wav python pydub runs/wav-pydub-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
