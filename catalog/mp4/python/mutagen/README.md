# mutagen — MP4 / Python

- **Pinned release:** `1.48.1`
- **License:** GPL-2.0-or-later
- **Parsed scope:** MP4 title metadata
- **Underlying family:** Mutagen MP4 parser
- **Local input API:** `mutagen.mp4.MP4(local path)`
- **Documentation:** [API reference](<https://mutagen.readthedocs.io/en/latest/api/mp4.html>)
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
