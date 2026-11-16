# mediainfo.js — WAV / JavaScript

- **Pinned release:** `0.3.8`
- **License:** BSD-2-Clause
- **Parsed scope:** header
- **Underlying family:** MediaInfoLib
- **Local input API:** `mediaInfoFactory().analyzeData(size, readChunk)`
- **Documentation:** [API reference](<https://mediainfo.js.org/docs/getting-started/usage/>)
- **Catalog evidence:** [parser record](../../../../data/javascript/wav/parsers.json) · [control verification](../../../../data/javascript/wav/verification.json) · [within-ecosystem ranking](../../../../data/javascript/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "bitsPerSample": 16
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/javascript/mediainfo_js/README.md)

```sh
python3 parsarium.py build wav javascript mediainfo_js
python3 parsarium.py run wav javascript mediainfo_js controls/wav/four-samples.wav
```
