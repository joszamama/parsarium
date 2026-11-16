# @isomp4/parser — MP4 / JavaScript

- **Pinned release:** `0.3.0`
- **License:** MPL-2.0
- **Parsed scope:** box_headers
- **Underlying family:** @isomp4/parser
- **Local input API:** `new MP4Parser().append(Uint8Array); boxStarted`
- **Documentation:** [API reference](<https://unpkg.com/@isomp4/parser@0.3.0/dist/parser.d.ts>)
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

[Docker harness and verification receipt](../../../../projects/mp4/javascript/isomp4_parser/README.md)

```sh
python3 parsarium.py build mp4 javascript isomp4_parser
python3 parsarium.py run mp4 javascript isomp4_parser controls/mp4/red-av.mp4
```
