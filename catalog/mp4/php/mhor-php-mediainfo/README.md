# mhor/php-mediainfo — MP4 / PHP

- **Pinned release:** `5.8.0`
- **Upstream:** [source repository](<https://github.com/mhor/php-mediainfo>) · [Packagist](<https://packagist.org/packages/mhor/php-mediainfo>)
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264/AVC video in MP4
- **Underlying family:** MediaInfoLib native MPEG-4 parser
- **Local input API:** `MediaInfo::getInfo(local MP4 path)->getVideos()[0]; AVC format and dimensions`
- **Documentation:** [API reference](<https://github.com/mhor/php-mediainfo/blob/a0be4ef4dc1f56292793ad31c2b3efc75bfdbf05/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_format": "AVC",
  "width": 2,
  "height": 2
}
```

PHP wrapper delegates to local MediaInfo 26.10 CLI; same release lock as PHP MP3/WAV cells.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/mhor_php_mediainfo/README.md)

```sh
python3 parsarium.py build mp4 php mhor_php_mediainfo
python3 parsarium.py run mp4 php mhor_php_mediainfo controls/mp4/red-av.mp4
```
