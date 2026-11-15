# audiostreamify/hvap — MP4 / PHP

- **Pinned release:** `0.1.1`
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264 video in MP4
- **Underlying family:** getID3 native QuickTime/MP4 parser
- **Local input API:** `Analyze local MP4 path through package getID3 adapter; return MP4 container and video dimensions/fourcc`
- **Documentation:** [API reference](<https://github.com/audiostreamify/hvap/blob/e9c0c63e9d7ed13f03b152c01452008b2076fc96/src/Mocks/ID3Tags.php>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mp4",
  "width": 2,
  "height": 2,
  "video_fourcc": "avc1"
}
```

Distinct Composer package path using getID3 QuickTime/MP4 parsing; shares the underlying getID3 family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
