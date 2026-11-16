# soundfile — WAV / Python

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/soundfile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python soundfile
python3 parsarium.py run wav python soundfile controls/wav/four-samples.wav
python3 parsarium.py replay wav python soundfile CORPUS_DIR runs/wav-soundfile-replay
python3 parsarium.py afl build wav python soundfile
python3 parsarium.py afl prepare wav python soundfile runs/wav-soundfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
