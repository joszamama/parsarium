# mp4tree — MP4 / JavaScript

- **Pinned release:** `0.10.4`
- **License:** MIT
- **Parsed scope:** box_tree
- **Underlying family:** mp4tree
- **Local input API:** `new MP4Tree(path).parse()`
- **Documentation:** [API reference](<https://unpkg.com/mp4tree@0.10.4/lib/mp4Tree.d.ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "valid": true,
  "boxes": [
    "ftyp",
    "moov",
    "free",
    "mdat"
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/mp4tree/README.md)

```sh
python3 parsarium.py build mp4 javascript mp4tree
python3 parsarium.py run mp4 javascript mp4tree controls/mp4/red-av.mp4
```
