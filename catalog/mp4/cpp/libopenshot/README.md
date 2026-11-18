# libopenshot — MP4 / C++

- **Pinned release:** `1.1.1`
- **Upstream:** [source repository](<https://github.com/OpenShot/libopenshot>) · [Debian](<https://tracker.debian.org/pkg/libopenshot>)
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

The verified libopenshot FFmpegReader route reaches pinned FFmpeg 9.0.2 libavformat MOV/MP4 parsing. It shares that syntax parser family with the MLT and FFmpeg package paths; libopenshot contributes a distinct documented C++ package API and reader. The AFL overlay scopes feedback to FFmpeg mov.c and libopenshot FFmpegReader.cpp.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/cpp/libopenshot/README.md)

```sh
python3 parsarium.py build mp4 cpp libopenshot
python3 parsarium.py run mp4 cpp libopenshot controls/mp4/red-av.mp4
```

**Coverage limit:** libopenshot's FFmpegReader opens media through libavformat, so it shares the FFmpeg MOV/MP4 parser family with the FFmpeg, MLT, and other FFmpeg-backed targets. The minimal Docker build enables only the H.264 and AAC decoders the control needs; other codecs leave codec fields null or disable the stream. AFL++ runs one process per local MP4 file through the replay binary.
