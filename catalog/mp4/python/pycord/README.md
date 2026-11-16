# pycord — MP4 / Python

- **Pinned release:** `0.1.1`
- **License:** MIT
- **Parsed scope:** decoded video frame
- **Underlying family:** pycord via FFmpeg and FFprobe
- **Local input API:** `pycord.video_reader.VideoReader(local path).get_range(0,1)`
- **Documentation:** [API reference](<https://pypi.org/project/pycord/0.1.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "frames": 1,
  "width": 2,
  "height": 2,
  "red_frame": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/pycord/README.md)

```sh
python3 parsarium.py build mp4 python pycord
python3 parsarium.py run mp4 python pycord controls/mp4/red-av.mp4
```
