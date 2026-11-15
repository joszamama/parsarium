# owen-oj/laravel-getid3 — MP4 / PHP

- **Pinned release:** `v2.6.0`
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264/AVC video in MP4
- **Underlying family:** getID3 native QuickTime/MP4 parser
- **Local input API:** `GetId3(local MP4 path)::extractInfo(); QuickTime/MP4 format, H.264 fourcc and dimensions`
- **Documentation:** [API reference](<https://github.com/Owen-oj/laravel-getid3/blob/6b89fc96b3dd2536fb2e53f8fee99ee6b76f9fd1/readme.md>)
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

Laravel wrapper delegates to pinned james-heinrich/getid3 in the same Composer lock; separate package path and shared QuickTime/MP4 family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
