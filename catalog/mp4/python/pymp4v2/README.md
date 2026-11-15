# pymp4v2 — MP4 / Python

- **Pinned release:** `0.1.13`
- **License:** MIT AND MPL-1.1
- **Parsed scope:** tracks, title, duration
- **Underlying family:** mp4v2 native binding
- **Local input API:** `pymp4v2.MP4File(local path, mode="r")`
- **Documentation:** [API reference](<https://pypi.org/project/pymp4v2/0.1.13/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "tracks": 2,
  "duration_seconds": 1.0
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
