# simple-id3.js — MP3 with ID3v2 / JavaScript

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/javascript/simple-id3-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript simple_id3_js
python3 parsarium.py run mp3_id3v2 javascript simple_id3_js controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript simple_id3_js CORPUS_DIR runs/mp3_id3v2-simple_id3_js-replay
python3 parsarium.py afl build mp3_id3v2 javascript simple_id3_js
python3 parsarium.py afl prepare mp3_id3v2 javascript simple_id3_js runs/mp3_id3v2-simple_id3_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
