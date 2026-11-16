# librosa — WAV / Python

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/librosa/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python librosa
python3 parsarium.py run wav python librosa controls/wav/four-samples.wav
python3 parsarium.py replay wav python librosa CORPUS_DIR runs/wav-librosa-replay
python3 parsarium.py afl build wav python librosa
python3 parsarium.py afl prepare wav python librosa runs/wav-librosa-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
