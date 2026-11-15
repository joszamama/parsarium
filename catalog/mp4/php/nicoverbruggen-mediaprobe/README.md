# nicoverbruggen/mediaprobe — MP4 / PHP

- **Pinned release:** `v1.1`
- **License:** MIT
- **Parsed scope:** MP4 container, two streams, and document title
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `MediaProbe(local MP4 path)::getMediaInfo(); MP4 container, stream count, and title`
- **Documentation:** [API reference](<https://github.com/nicoverbruggen/mediaprobe/blob/aa824d0691598dc9d66301f78da2687bc656884c/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "container": "mov,mp4,m4a,3gp,3g2,mj2",
  "streams": 2,
  "title": "Parsarium"
}
```

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
