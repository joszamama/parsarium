# moviepy — MP4 / Python

- **Pinned release:** `2.2.1`
- **License:** MIT
- **Parsed scope:** decoded video frame and duration
- **Underlying family:** MoviePy via FFmpeg
- **Local input API:** `moviepy.VideoFileClip(local path)`
- **Documentation:** [API reference](<https://github.com/Zulko/moviepy/blob/master/moviepy/video/io/VideoFileClip.py>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "duration_seconds": 1.0,
  "red_frame": true
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
