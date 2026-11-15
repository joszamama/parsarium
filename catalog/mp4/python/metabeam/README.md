# metabeam — MP4 / Python

- **Pinned release:** `0.1.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP4 brands, timescale, box list
- **Underlying family:** metabeam Rust MP4 parser
- **Local input API:** `metabeam.parse(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/metabeam/0.1.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "major_brand": "isom",
  "timescale": 8000,
  "boxes": [
    "ftyp",
    "moov",
    "free",
    "mdat"
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
