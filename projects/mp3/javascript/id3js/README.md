# id3js — MP3 / JavaScript

Pinned release: `2.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/id3js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript id3js
python3 parsarium.py run mp3_id3v2 javascript id3js controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript id3js CORPUS_DIR runs/mp3_id3v2-id3js-replay
python3 parsarium.py afl build mp3_id3v2 javascript id3js
python3 parsarium.py afl prepare mp3_id3v2 javascript id3js runs/mp3_id3v2-id3js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
