# avcpp — MP4 / C++

- **Pinned release:** `3.0.1`
- **License:** BSD-3-Clause OR LGPL-2.1-only
- **Parsed scope:** MP4 demuxer and one video plus one audio stream
- **Underlying family:** AvCpp API over FFmpeg MOV/MP4 demuxer
- **Local input API:** `av::FormatContext::openInput(local MP4 filename); findStreamInfo; inputFormat; stream(index)`
- **Documentation:** [API reference](<https://h4tr3d.github.io/avcpp/formatcontext_8h_source.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mp4",
  "streams": 2,
  "video": 1,
  "audio": 1
}
```

Distinct published C++ package/API built against the pinned FFmpeg 9.0.2 libraries; shares the already recorded FFmpeg parser engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
