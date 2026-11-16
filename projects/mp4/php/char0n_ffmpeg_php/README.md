# char0n/ffmpeg-php — MP4 / PHP

Pinned release: `3.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/char0n-ffmpeg-php/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php char0n_ffmpeg_php
python3 parsarium.py run mp4 php char0n_ffmpeg_php controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php char0n_ffmpeg_php CORPUS_DIR runs/mp4-char0n_ffmpeg_php-replay
python3 parsarium.py afl build mp4 php char0n_ffmpeg_php
python3 parsarium.py afl prepare mp4 php char0n_ffmpeg_php runs/mp4-char0n_ffmpeg_php-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
