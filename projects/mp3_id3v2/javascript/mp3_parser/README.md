# mp3-parser — MP3 with ID3v2 / JavaScript

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/javascript/mp3-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript mp3_parser
python3 parsarium.py run mp3_id3v2 javascript mp3_parser controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript mp3_parser CORPUS_DIR runs/mp3_id3v2-mp3_parser-replay
python3 parsarium.py afl build mp3_id3v2 javascript mp3_parser
python3 parsarium.py afl prepare mp3_id3v2 javascript mp3_parser runs/mp3_id3v2-mp3_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
