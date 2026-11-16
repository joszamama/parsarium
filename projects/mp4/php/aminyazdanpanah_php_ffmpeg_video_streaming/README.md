# aminyazdanpanah/php-ffmpeg-video-streaming — MP4 / PHP

Pinned release: `v1.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/aminyazdanpanah-php-ffmpeg-video-streaming/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php aminyazdanpanah_php_ffmpeg_video_streaming
python3 parsarium.py run mp4 php aminyazdanpanah_php_ffmpeg_video_streaming controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php aminyazdanpanah_php_ffmpeg_video_streaming CORPUS_DIR runs/mp4-aminyazdanpanah_php_ffmpeg_video_streaming-replay
python3 parsarium.py afl build mp4 php aminyazdanpanah_php_ffmpeg_video_streaming
python3 parsarium.py afl prepare mp4 php aminyazdanpanah_php_ffmpeg_video_streaming runs/mp4-aminyazdanpanah_php_ffmpeg_video_streaming-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
