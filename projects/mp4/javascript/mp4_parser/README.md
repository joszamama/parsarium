# mp4-parser — MP4 / JavaScript

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/mp4-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript mp4_parser
python3 parsarium.py run mp4 javascript mp4_parser controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript mp4_parser CORPUS_DIR runs/mp4-mp4_parser-replay
python3 parsarium.py afl build mp4 javascript mp4_parser
python3 parsarium.py afl prepare mp4 javascript mp4_parser runs/mp4-mp4_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
