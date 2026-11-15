# libopenshot — MP4 / C++

- **Pinned release:** `1.1.1`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** FFmpegReader opened a valid MP4, reporting H.264 video, AAC audio and 2x2 dimensions
- **Underlying family:** OpenShot FFmpegReader over FFmpeg MOV/MP4 demuxer
- **Local input API:** `openshot::FFmpegReader(local MP4 filename); Open(); ReaderInfo::has_video/has_audio/width/height/vcodec/acodec`
- **Documentation:** [API reference](<https://github.com/OpenShot/libopenshot/blob/v1.1.1/src/FFmpegReader.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video": 1,
  "audio": 1,
  "width": 2,
  "height": 2,
  "video_codec": "h264",
  "audio_codec": "aac"
}
```

Distinct tagged OpenShot C++ package/API, built with tagged OpenShotAudio; FFmpegReader uses libavformat and shares the existing FFmpeg parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
