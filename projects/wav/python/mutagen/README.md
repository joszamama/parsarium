# mutagen — WAV / Python

Pinned release: `1.48.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/mutagen/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python mutagen
python3 parsarium.py run wav python mutagen controls/wav/four-samples.wav
python3 parsarium.py replay wav python mutagen CORPUS_DIR runs/wav-mutagen-replay
python3 parsarium.py afl build wav python mutagen
python3 parsarium.py afl prepare wav python mutagen runs/wav-mutagen-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
