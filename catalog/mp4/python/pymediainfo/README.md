# pymediainfo — MP4 / Python

- **Pinned release:** `7.0.1`
- **License:** MIT
- **Parsed scope:** video/audio track metadata
- **Underlying family:** MediaInfo native MP4 parser
- **Local input API:** `pymediainfo.MediaInfo.parse(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/pymediainfo/7.0.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "video_format": "AVC",
  "audio_format": "AAC"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/pymediainfo/README.md)

```sh
python3 parsarium.py build mp4 python pymediainfo
python3 parsarium.py run mp4 python pymediainfo controls/mp4/red-av.mp4
```
