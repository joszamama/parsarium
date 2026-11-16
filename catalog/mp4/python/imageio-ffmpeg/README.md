# imageio-ffmpeg — MP4 / Python

- **Pinned release:** `0.8.1`
- **License:** BSD-2-Clause
- **Parsed scope:** decoded video frame and codec
- **Underlying family:** imageio-ffmpeg via bundled FFmpeg
- **Local input API:** `imageio_ffmpeg.read_frames(local path)`
- **Documentation:** [API reference](<https://github.com/imageio/imageio-ffmpeg>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "video_codec": "h264",
  "red_frame": true
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
