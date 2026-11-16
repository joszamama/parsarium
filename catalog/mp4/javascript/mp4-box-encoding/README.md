# mp4-box-encoding — MP4 / JavaScript

- **Pinned release:** `1.4.1`
- **License:** MIT
- **Parsed scope:** ftyp
- **Underlying family:** mp4-box-encoding
- **Local input API:** `decode(Buffer containing ftyp box)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp4-box-encoding>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "type": "ftyp",
  "brand": "isom",
  "compatible": [
    "isom",
    "iso2",
    "avc1",
    "mp41"
  ]
}
```

Parses the ftyp box only; narrow container-header scope.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/mp4_box_encoding/README.md)

```sh
python3 parsarium.py build mp4 javascript mp4_box_encoding
python3 parsarium.py run mp4 javascript mp4_box_encoding controls/mp4/red-av.mp4
```
