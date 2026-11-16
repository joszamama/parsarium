# fmp4.js — MP4 / JavaScript

- **Pinned release:** `0.2.2`
- **License:** MIT
- **Parsed scope:** box_headers
- **Underlying family:** fmp4.js
- **Local input API:** `parse().end(Buffer); boxes`
- **Documentation:** [API reference](<https://www.npmjs.com/package/fmp4.js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "boxes": [
    "ftyp",
    "moov",
    "free",
    "mdat"
  ]
}
```

Parses top-level MP4 box headers only in this control.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/fmp4_js/README.md)

```sh
python3 parsarium.py build mp4 javascript fmp4_js
python3 parsarium.py run mp4 javascript fmp4_js controls/mp4/red-av.mp4
```
