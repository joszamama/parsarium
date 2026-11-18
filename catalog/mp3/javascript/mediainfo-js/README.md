# mediainfo.js — MP3 / JavaScript

- **Pinned release:** `0.3.8`
- **Upstream:** [source repository](<https://github.com/buzz/mediainfo.js>) · [npm](<https://www.npmjs.com/package/mediainfo.js>)
- **License:** BSD-2-Clause
- **Parsed scope:** tags
- **Underlying family:** MediaInfoLib WASM
- **Local input API:** `MediaInfo().analyzeData(size,readChunk)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mediainfo.js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/javascript/mediainfo_js/README.md)

```sh
python3 parsarium.py build mp3 javascript mediainfo_js
python3 parsarium.py run mp3 javascript mediainfo_js controls/mp3/id3v2-tagged-tone.mp3
```
