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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/c/mlt/README.md)

```sh
python3 parsarium.py build mp4 c mlt
python3 parsarium.py run mp4 c mlt controls/mp4/red-av.mp4
```

**Coverage limit:** MLT C and C++ paths share the avformat plugin and FFmpeg MOV/MP4 parser family. The minimal Docker build enables H.264 and AAC decoders for the control, with null codec fields possible for other codecs. AFL++ runs one process per local MP4 file because MLT loads and closes global plugins.
