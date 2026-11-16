# char0n/ffmpeg-php — MP4 / PHP

- **Pinned release:** `3.2.2`
- **License:** BSD-3-Clause
- **Parsed scope:** H.264 video and one-second duration
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `Movie(local MP4 path); video codec and duration`
- **Documentation:** [API reference](<https://github.com/char0n/ffmpeg-php/blob/9a38fdc2a3b2bf2d5df9d28a571f05a1e71c0cf8/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_codec": "h264",
  "duration_seconds": 1
}
```

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/char0n_ffmpeg_php/README.md)

```sh
python3 parsarium.py build mp4 php char0n_ffmpeg_php
python3 parsarium.py run mp4 php char0n_ffmpeg_php controls/mp4/red-av.mp4
```
