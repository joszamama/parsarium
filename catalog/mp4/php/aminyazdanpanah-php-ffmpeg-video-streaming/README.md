# aminyazdanpanah/php-ffmpeg-video-streaming — MP4 / PHP

- **Pinned release:** `v1.3.1`
- **Upstream:** [source repository](<https://github.com/quasarstream/PHP-FFmpeg-video-streaming>) · [Packagist](<https://packagist.org/packages/aminyazdanpanah/php-ffmpeg-video-streaming>)
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264 video in MP4
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `Streaming\FFMpeg::open(local MP4 path)->getStreams()->videos()->first(); codec and dimensions`
- **Documentation:** [API reference](<https://github.com/quasarstream/PHP-FFmpeg-video-streaming/blob/f35173fde44bef3c683b9bb4aaee57221dd79771/README.md>)
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

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family. PHP 8.5 emits deprecation notices on load, while the valid control returns the expected result.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/aminyazdanpanah_php_ffmpeg_video_streaming/README.md)

```sh
python3 parsarium.py build mp4 php aminyazdanpanah_php_ffmpeg_video_streaming
python3 parsarium.py run mp4 php aminyazdanpanah_php_ffmpeg_video_streaming controls/mp4/red-av.mp4
```
