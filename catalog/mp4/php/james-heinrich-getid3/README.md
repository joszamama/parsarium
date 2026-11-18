# james-heinrich/getid3 — MP4 / PHP

- **Pinned release:** `v1.9.28`
- **Upstream:** [source repository](<https://github.com/JamesHeinrich/getID3>) · [Packagist](<https://packagist.org/packages/james-heinrich/getid3>)
- **License:** GPL-1.0-or-later OR LGPL-3.0-only OR MPL-2.0
- **Parsed scope:** 2 × 2 H.264 video in MP4 with one AAC mono audio stream
- **Underlying family:** getID3 native QuickTime/MP4 parser
- **Local input API:** `getID3::analyze(local MP4 path); QuickTime/MP4 file format, H.264 fourcc, dimensions and AAC channel count`
- **Documentation:** [API reference](<https://github.com/JamesHeinrich/getID3/blob/be83ea6ffbdac0301d83bee0d42f09e2a41bd0dd/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mp4",
  "width": 2,
  "height": 2,
  "video_fourcc": "avc1",
  "audio_channels": 1
}
```

Own QuickTime/MP4 atom parser; same pinned release and lock shared with PHP MP3/WAV cells.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/getid3/README.md)

```sh
python3 parsarium.py build mp4 php getid3
python3 parsarium.py run mp4 php getid3 controls/mp4/red-av.mp4
```
