# rasuvaeff/media-converter — MP4 / PHP

- **Pinned release:** `v1.2.0`
- **License:** BSD-3-Clause
- **Parsed scope:** 2 × 2 H.264 video and one-second duration
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `FfprobeMediaInfo::probe(local MP4 path); H.264 codec, dimensions, and duration`
- **Documentation:** [API reference](<https://github.com/rasuvaeff/media-converter/blob/68ad862a4c6583ed5555a5815ee9bc0bd0568da4/src/FfprobeMediaInfo.php>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_codec": "h264",
  "width": 2,
  "height": 2,
  "duration_seconds": 1
}
```

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
