# wavfile — WAV / Python

Pinned release: `5.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/wavfile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python wavfile
python3 parsarium.py run wav python wavfile controls/wav/four-samples.wav
python3 parsarium.py replay wav python wavfile CORPUS_DIR runs/wav-wavfile-replay
python3 parsarium.py afl build wav python wavfile
python3 parsarium.py afl prepare wav python wavfile runs/wav-wavfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
