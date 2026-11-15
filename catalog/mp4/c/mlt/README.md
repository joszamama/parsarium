# mlt — MP4 / C

- **Pinned release:** `7.42.0`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** AVFormat producer parsed MP4 video/audio codecs and 2x2 video dimensions
- **Underlying family:** MLT avformat producer over FFmpeg MOV/MP4 demuxer
- **Local input API:** `mlt_factory_producer(profile, "avformat", local filename); mlt_producer_properties`
- **Documentation:** [API reference](<https://mltframework.org/docs/framework/>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "streams": 2,
  "video_codec": "h264",
  "audio_codec": "aac",
  "width": 2,
  "height": 2
}
```

MLT C and C++ package APIs use the same MLT avformat plugin; the plugin links FFmpeg 9.0.2 libavformat, sharing the existing FFmpeg parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
