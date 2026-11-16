# minuteoflaravel/laravel-audio-video-validator — MP4 / PHP

- **Pinned release:** `1.1`
- **License:** MIT
- **Parsed scope:** 2 × 2 H.264 video in MP4
- **Underlying family:** FFmpeg native MOV/MP4 parser
- **Local input API:** `MediaValidator::validateVideo(local MP4 path), getVideoStream(); H.264 codec and dimensions`
- **Documentation:** [API reference](<https://github.com/minuteoflaravel/laravel-audio-video-validator/blob/c754b81f825342faa29252cbecea5b37b67ec4e9/src/MediaValidator.php>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "is_video": true,
  "video_codec": "h264",
  "width": 2,
  "height": 2
}
```

Distinct PHP package path delegating local MP4 inspection to FFmpeg ffprobe 9.0.2; shared native parser family. illuminate/validation v13.42.0 is an explicit companion dependency for its validation trait.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/php/minuteoflaravel_laravel_audio_video_validator/README.md)

```sh
python3 parsarium.py build mp4 php minuteoflaravel_laravel_audio_video_validator
python3 parsarium.py run mp4 php minuteoflaravel_laravel_audio_video_validator controls/mp4/red-av.mp4
```
