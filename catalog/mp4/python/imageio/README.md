# imageio — MP4 / Python

- **Pinned release:** `2.38.1`
- **License:** BSD-2-Clause
- **Parsed scope:** decoded video frame and codec
- **Underlying family:** ImageIO via imageio-ffmpeg/FFmpeg
- **Local input API:** `imageio.get_reader(local path)`
- **Documentation:** [API reference](<https://imageio.readthedocs.io/en/stable/reference/userapi.html>)
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
