# mp3tag.js — MP3 with ID3v2 / JavaScript

Pinned release: `3.17.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/javascript/mp3tag-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript mp3tag_js
python3 parsarium.py run mp3_id3v2 javascript mp3tag_js controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript mp3tag_js CORPUS_DIR runs/mp3_id3v2-mp3tag_js-replay
python3 parsarium.py afl build mp3_id3v2 javascript mp3tag_js
python3 parsarium.py afl prepare mp3_id3v2 javascript mp3tag_js runs/mp3_id3v2-mp3tag_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
