# wavefile-parser — WAV / JavaScript

Pinned release: `1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/wavefile-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript wavefile_parser
python3 parsarium.py run wav javascript wavefile_parser controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript wavefile_parser CORPUS_DIR runs/wav-wavefile_parser-replay
python3 parsarium.py afl build wav javascript wavefile_parser
python3 parsarium.py afl prepare wav javascript wavefile_parser runs/wav-wavefile_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
