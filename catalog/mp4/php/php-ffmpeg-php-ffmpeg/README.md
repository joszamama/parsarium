# php-ffmpeg/php-ffmpeg — MP4 / PHP

- **Pinned release:** `v1.4.0`
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264/AVC video in MP4
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `FFProbe::streams(local MP4 path)->videos()->first(); H.264 codec, fourcc and dimensions`
- **Documentation:** [API reference](<https://github.com/PHP-FFMpeg/PHP-FFMpeg/blob/41fa00949ea2758cd34f076a8030df7198d57759/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_codec": "h264",
  "width": 2,
  "height": 2,
  "video_fourcc": "avc1"
}
```

PHP FFProbe wrapper delegates to local FFmpeg 9.0.2; shares native parser family with buggedcom/phpvideotoolkit.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/php_ffmpeg_php_ffmpeg/README.md)

```sh
python3 parsarium.py build mp4 php php_ffmpeg_php_ffmpeg
python3 parsarium.py run mp4 php php_ffmpeg_php_ffmpeg controls/mp4/red-av.mp4
```
