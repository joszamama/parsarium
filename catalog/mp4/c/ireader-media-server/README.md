# ireader-media-server — MP4 / C

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parsed scope:** One video and one audio track, 2x2 video dimensions and 1000 ms duration from valid MP4
- **Underlying family:** ireader libmov native ISO BMFF/MOV reader
- **Local input API:** `mov_reader_create(mov_file_buffer(), local FILE*); mov_reader_getinfo callbacks; mov_reader_getduration`
- **Documentation:** [API reference](<https://github.com/ireader/media-server/blob/v1.0.0/libmov/include/mov-reader.h>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_tracks": 1,
  "audio_tracks": 1,
  "width": 2,
  "height": 2,
  "duration_ms": 1000
}
```

C and C++ adapters call the same tagged libmov C parser and upstream FILE callback adapter; counted as one underlying parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
