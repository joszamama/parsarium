# buggedcom/phpvideotoolkit — MP4 / PHP

- **Pinned release:** `2.2.5`
- **Upstream:** [source repository](<https://github.com/buggedcom/phpvideotoolkit-v2>) · [Packagist](<https://packagist.org/packages/buggedcom/phpvideotoolkit>)
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264/AVC video in MP4
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `MediaParser::getFileInformation(local MP4 path); container, H.264 codec and dimensions`
- **Documentation:** [API reference](<https://github.com/buggedcom/phpvideotoolkit-v2/blob/383a5b2c0ee7f4de4efea9a9154bb693630bbe0f/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "container": "mov,mp4,m4a,3gp,3g2,mj2",
  "video_codec": "h264",
  "width": 2,
  "height": 2
}
```

PHP wrapper delegates to local FFmpeg 9.0.2; same release lock as PHP MP3/WAV cells.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/buggedcom_phpvideotoolkit/README.md)

```sh
python3 parsarium.py build mp4 php buggedcom_phpvideotoolkit
python3 parsarium.py run mp4 php buggedcom_phpvideotoolkit controls/mp4/red-av.mp4
```
