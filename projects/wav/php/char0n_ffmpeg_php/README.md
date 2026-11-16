# char0n/ffmpeg-php — WAV / PHP

Pinned release: `3.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/char0n-ffmpeg-php/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php char0n_ffmpeg_php
python3 parsarium.py run wav php char0n_ffmpeg_php controls/wav/256-samples.wav
python3 parsarium.py replay wav php char0n_ffmpeg_php CORPUS_DIR runs/wav-char0n_ffmpeg_php-replay
python3 parsarium.py afl build wav php char0n_ffmpeg_php
python3 parsarium.py afl prepare wav php char0n_ffmpeg_php runs/wav-char0n_ffmpeg_php-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
