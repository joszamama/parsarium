# audiolab — WAV / Python

Pinned release: `0.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/audiolab/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python audiolab
python3 parsarium.py run wav python audiolab controls/wav/four-samples.wav
python3 parsarium.py replay wav python audiolab CORPUS_DIR runs/wav-audiolab-replay
python3 parsarium.py afl build wav python audiolab
python3 parsarium.py afl prepare wav python audiolab runs/wav-audiolab-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
