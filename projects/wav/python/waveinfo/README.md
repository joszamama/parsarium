# waveinfo — WAV / Python

Pinned release: `0.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/waveinfo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python waveinfo
python3 parsarium.py run wav python waveinfo controls/wav/four-samples.wav
python3 parsarium.py replay wav python waveinfo CORPUS_DIR runs/wav-waveinfo-replay
python3 parsarium.py afl build wav python waveinfo
python3 parsarium.py afl prepare wav python waveinfo runs/wav-waveinfo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
