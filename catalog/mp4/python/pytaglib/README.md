# pytaglib — MP4 / Python

- **Pinned release:** `3.2.0`
- **License:** GPL-3.0-or-later
- **Parsed scope:** MP4 title metadata
- **Underlying family:** TagLib native MP4 parser
- **Local input API:** `taglib.File(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/pytaglib/3.2.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
