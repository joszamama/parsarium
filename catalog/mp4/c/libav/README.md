# libav — MP4 / C

- **Pinned release:** `12.3`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** MP4 major brand, two track types and 2x2 video dimensions
- **Underlying family:** Libav MOV/MP4 demuxer, forked from FFmpeg
- **Local input API:** `av_register_all; avformat_open_input(local MP4 path); avformat_find_stream_info; AVStream.codecpar and container metadata`
- **Documentation:** [API reference](<https://github.com/libav/libav/blob/v12.3/libavformat/avformat.h>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom",
  "tracks": 2,
  "video": 1,
  "audio": 1,
  "width": 2,
  "height": 2
}
```

Libav is a distinct release and package API implementation from FFmpeg 9.0.2 but descends from the same FFmpeg codebase; the adapter builds its own static Libav 12.3 libraries, with no linked FFmpeg binary. This is one path, not independent parser-family diversity.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
