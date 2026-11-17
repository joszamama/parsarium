# mp3-parser — MP3 / JavaScript

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, parser family and limits](../../../../catalog/mp3/javascript/mp3-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 javascript mp3_parser
python3 parsarium.py run mp3 javascript mp3_parser controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 javascript mp3_parser CORPUS_DIR runs/mp3-mp3_parser-replay
python3 parsarium.py afl build mp3 javascript mp3_parser
python3 parsarium.py afl prepare mp3 javascript mp3_parser runs/mp3-mp3_parser-afl
```

Replace `CORPUS_DIR` with a directory of MP3 files. The AFL++ command prepares a seeded run; it does not start a campaign. Feedback is scoped to the package's `lib/lib.js` frame reader.
