# mediainfo.js — MP3 / JavaScript

Pinned release: `0.3.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/mediainfo-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript mediainfo_js
python3 parsarium.py run mp3_id3v2 javascript mediainfo_js controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript mediainfo_js CORPUS_DIR runs/mp3_id3v2-mediainfo_js-replay
python3 parsarium.py afl build mp3_id3v2 javascript mediainfo_js
python3 parsarium.py afl prepare mp3_id3v2 javascript mediainfo_js runs/mp3_id3v2-mediainfo_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
