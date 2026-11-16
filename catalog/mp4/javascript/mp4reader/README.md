# mp4reader — MP4 / JavaScript

- **Pinned release:** `0.1.6`
- **License:** ISC
- **Parsed scope:** brand+handlers
- **Underlying family:** mp4reader
- **Local input API:** `Mp4DecodeByModule(path,[ftyp,hdlr])`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp4reader>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom",
  "handlers": [
    "vide",
    "soun"
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/mp4reader/README.md)

```sh
python3 parsarium.py build mp4 javascript mp4reader
python3 parsarium.py run mp4 javascript mp4reader controls/mp4/red-av.mp4
```
