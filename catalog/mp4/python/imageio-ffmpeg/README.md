# imageio-ffmpeg — MP4 / Python

- **Pinned release:** `0.8.1`
- **Upstream:** [source repository](<https://github.com/imageio/imageio-ffmpeg>) · [PyPI](<https://pypi.org/project/imageio-ffmpeg/>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/imageio_ffmpeg/README.md)

```sh
python3 parsarium.py build mp4 python imageio_ffmpeg
python3 parsarium.py run mp4 python imageio_ffmpeg controls/mp4/red-av.mp4
```
