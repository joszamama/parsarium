# uberchel/mediainfo4php — MP4 / PHP

Pinned release: `v1.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/uberchel-mediainfo4php/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php uberchel_mediainfo4php
python3 parsarium.py run mp4 php uberchel_mediainfo4php controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php uberchel_mediainfo4php CORPUS_DIR runs/mp4-uberchel_mediainfo4php-replay
python3 parsarium.py afl build mp4 php uberchel_mediainfo4php
python3 parsarium.py afl prepare mp4 php uberchel_mediainfo4php runs/mp4-uberchel_mediainfo4php-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
