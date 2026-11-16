# mediainfo.js — WAV / JavaScript

Pinned release: `0.3.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/mediainfo-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript mediainfo_js
python3 parsarium.py run wav javascript mediainfo_js controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript mediainfo_js CORPUS_DIR runs/wav-mediainfo_js-replay
python3 parsarium.py afl build wav javascript mediainfo_js
python3 parsarium.py afl prepare wav javascript mediainfo_js runs/wav-mediainfo_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
