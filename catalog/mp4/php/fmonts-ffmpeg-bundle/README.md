# fmonts/ffmpeg-bundle — MP4 / PHP

- **Pinned release:** `0.8.7`
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264 video in MP4
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `Bundle-registered FFProbe service streams(local MP4 path)->videos()->first(); codec and dimensions`
- **Documentation:** [API reference](<https://github.com/fmonts/ffmpeg-bundle/blob/c1da20c03de127a93fa021addf80d2108f933ac1/Resources/config/factories.php>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "video_codec": "h264",
  "width": 2,
  "height": 2
}
```

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family. The pinned bundle registers the FFProbe service through Symfony DI.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/fmonts_ffmpeg_bundle/README.md)

```sh
python3 parsarium.py build mp4 php fmonts_ffmpeg_bundle
python3 parsarium.py run mp4 php fmonts_ffmpeg_bundle controls/mp4/red-av.mp4
```
