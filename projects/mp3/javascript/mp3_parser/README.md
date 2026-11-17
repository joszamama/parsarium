# mp3-parser — MP3 / JavaScript

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/mp3-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 javascript mp3_parser
python3 parsarium.py run mp3 javascript mp3_parser controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 javascript mp3_parser CORPUS_DIR runs/mp3-mp3_parser-replay
python3 parsarium.py afl build mp3 javascript mp3_parser
python3 parsarium.py afl prepare mp3 javascript mp3_parser runs/mp3-mp3_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III CBR controls only; frame metadata, no Layer III audio decode. Two valid controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5, CRC-protected or ID3 behavior.
