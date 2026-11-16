# miniaudio — WAV / Python

Pinned release: `1.73`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/miniaudio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python miniaudio
python3 parsarium.py run wav python miniaudio controls/wav/four-samples.wav
python3 parsarium.py replay wav python miniaudio CORPUS_DIR runs/wav-miniaudio-replay
python3 parsarium.py afl build wav python miniaudio
python3 parsarium.py afl prepare wav python miniaudio runs/wav-miniaudio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
