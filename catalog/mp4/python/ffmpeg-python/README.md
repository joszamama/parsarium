# ffmpeg-python — MP4 / Python

- **Pinned release:** `0.2.0`
- **License:** Apache-2.0
- **Parsed scope:** video dimensions, codec, title
- **Underlying family:** ffmpeg-python via external FFprobe
- **Local input API:** `ffmpeg.probe(local path)`
- **Documentation:** [API reference](<https://github.com/kkroening/ffmpeg-python>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "width": 2,
  "height": 2,
  "video_codec": "h264"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/ffmpeg_python/README.md)

```sh
python3 parsarium.py build mp4 python ffmpeg_python
python3 parsarium.py run mp4 python ffmpeg_python controls/mp4/red-av.mp4
```
