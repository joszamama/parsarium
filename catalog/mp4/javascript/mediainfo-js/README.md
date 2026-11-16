# mediainfo.js — MP4 / JavaScript

- **Pinned release:** `0.3.8`
- **License:** BSD-2-Clause
- **Parsed scope:** tracks+title
- **Underlying family:** MediaInfoLib WASM
- **Local input API:** `MediaInfo().analyzeData(size,readChunk)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mediainfo.js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "width": 2,
  "height": 2,
  "sampleRate": 8000
}
```

WebAssembly distribution of MediaInfoLib; same family as native MediaInfo.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/mediainfo_js/README.md)

```sh
python3 parsarium.py build mp4 javascript mediainfo_js
python3 parsarium.py run mp4 javascript mediainfo_js controls/mp4/red-av.mp4
```
