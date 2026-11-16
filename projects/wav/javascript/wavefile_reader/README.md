# wavefile-reader — WAV / JavaScript

Pinned release: `1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/wavefile-reader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript wavefile_reader
python3 parsarium.py run wav javascript wavefile_reader controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript wavefile_reader CORPUS_DIR runs/wav-wavefile_reader-replay
python3 parsarium.py afl build wav javascript wavefile_reader
python3 parsarium.py afl prepare wav javascript wavefile_reader runs/wav-wavefile_reader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
