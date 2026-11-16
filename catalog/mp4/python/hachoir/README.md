# hachoir — MP4 / Python

- **Pinned release:** `3.4.0`
- **License:** GPL-2.0-only
- **Parsed scope:** video dimensions and duration
- **Underlying family:** Hachoir QuickTime/MP4 parser
- **Local input API:** `hachoir.parser.createParser(local path); extractMetadata`
- **Documentation:** [API reference](<https://hachoir.readthedocs.io/en/latest/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "duration_seconds": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
