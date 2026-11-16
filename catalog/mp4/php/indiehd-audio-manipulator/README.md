# indiehd/audio-manipulator — MP4 / PHP

- **Pinned release:** `v4.1.0`
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264 video in MP4
- **Underlying family:** getID3 native QuickTime/MP4 parser
- **Local input API:** `Analyze local MP4 path through package getID3 adapter; return MP4 container and video dimensions/fourcc`
- **Documentation:** [API reference](<https://github.com/indiehd/audio-manipulator/blob/1e2f6d76030200c77cd727b40d3ea6166957f45d/src/MediaParsing/MediaParserInterface.php>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mp4",
  "width": 2,
  "height": 2,
  "video_fourcc": "avc1"
}
```

Distinct Composer package path using getID3 QuickTime/MP4 parsing; shares the underlying getID3 family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/indiehd_audio_manipulator/README.md)

```sh
python3 parsarium.py build mp4 php indiehd_audio_manipulator
python3 parsarium.py run mp4 php indiehd_audio_manipulator controls/mp4/red-av.mp4
```
