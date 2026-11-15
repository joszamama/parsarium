# libquicktime — MP4 / C++

- **Pinned release:** `1.2.4`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** MP4 video/audio track counts and 2x2 video dimensions from parsed atoms
- **Underlying family:** libquicktime native QuickTime/MP4 atom reader
- **Local input API:** `quicktime_open(local MP4 filename, 1, 0); quicktime_video_tracks; quicktime_audio_tracks; quicktime_video_width/height`
- **Documentation:** [API reference](<https://libquicktime.sourceforge.net/introduction.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_tracks": 1,
  "audio_tracks": 1,
  "width": 2,
  "height": 2
}
```

C and C++ adapters call the same pinned libquicktime C API. Codec decode plugins are not required for the container result.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
