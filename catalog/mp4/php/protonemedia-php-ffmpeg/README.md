# protonemedia/php-ffmpeg — MP4 / PHP

- **Pinned release:** `v1.2.0`
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264 video in MP4
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `FFProbe::streams(local MP4 path)->videos()->first(); H.264 codec, fourcc, dimensions`
- **Documentation:** [API reference](<https://github.com/protonemedia/PHP-FFMpeg/blob/4c52b1ce23b9980795dedc95a7958d972b47ada5/README.md>)
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

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/protonemedia_php_ffmpeg/README.md)

```sh
python3 parsarium.py build mp4 php protonemedia_php_ffmpeg
python3 parsarium.py run mp4 php protonemedia_php_ffmpeg controls/mp4/red-av.mp4
```
