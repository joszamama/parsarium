# mediabunny — MP4 / JavaScript

- **Pinned release:** `1.65.2`
- **Upstream:** [source repository](<https://github.com/Vanilagy/mediabunny>) · [npm](<https://www.npmjs.com/package/mediabunny>)
- **License:** MPL-2.0
- **Parsed scope:** tracks+duration
- **Underlying family:** mediabunny
- **Local input API:** `Input({source:BufferSource(Uint8Array),formats:ALL_FORMATS}).getTracks()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mediabunny>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "MP4",
  "duration": 1,
  "width": 2,
  "height": 2,
  "audioCodec": "aac"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/mediabunny/README.md)

```sh
python3 parsarium.py build mp4 javascript mediabunny
python3 parsarium.py run mp4 javascript mediabunny controls/mp4/red-av.mp4
```
