# uberchel/mediainfo4php — WAV / PHP

Pinned release: `v1.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/uberchel-mediainfo4php/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php uberchel_mediainfo4php
python3 parsarium.py run wav php uberchel_mediainfo4php controls/wav/256-samples.wav
python3 parsarium.py replay wav php uberchel_mediainfo4php CORPUS_DIR runs/wav-uberchel_mediainfo4php-replay
python3 parsarium.py afl build wav php uberchel_mediainfo4php
python3 parsarium.py afl prepare wav php uberchel_mediainfo4php runs/wav-uberchel_mediainfo4php-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
