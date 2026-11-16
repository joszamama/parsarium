# pymediainfo — WAV / Python

Pinned release: `7.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/pymediainfo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python pymediainfo
python3 parsarium.py run wav python pymediainfo controls/wav/four-samples.wav
python3 parsarium.py replay wav python pymediainfo CORPUS_DIR runs/wav-pymediainfo-replay
python3 parsarium.py afl build wav python pymediainfo
python3 parsarium.py afl prepare wav python pymediainfo runs/wav-pymediainfo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
