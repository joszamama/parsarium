# mediainfo.js — MP4 / JavaScript

Pinned release: `0.3.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/mediainfo-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript mediainfo_js
python3 parsarium.py run mp4 javascript mediainfo_js controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript mediainfo_js CORPUS_DIR runs/mp4-mediainfo_js-replay
python3 parsarium.py afl build mp4 javascript mediainfo_js
python3 parsarium.py afl prepare mp4 javascript mediainfo_js runs/mp4-mediainfo_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
