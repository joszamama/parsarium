# uberchel/mediainfo4php — MP4 / PHP

- **Pinned release:** `v1.0.8`
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264 video and title
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `MediaInfo::Get(local MP4 path, false); H.264 video codec, dimensions, title`
- **Documentation:** [API reference](<https://github.com/uberchel/MediaInfo4PHP/blob/f0a168902117e0094a90b94501f006965c9aabc2/ReadMe.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_codec": "h264",
  "width": 2,
  "height": 2,
  "title": "Parsarium"
}
```

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/uberchel_mediainfo4php/README.md)

```sh
python3 parsarium.py build mp4 php uberchel_mediainfo4php
python3 parsarium.py run mp4 php uberchel_mediainfo4php controls/mp4/red-av.mp4
```
