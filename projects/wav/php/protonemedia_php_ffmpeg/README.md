# protonemedia/php-ffmpeg — WAV / PHP

Pinned release: `v1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/protonemedia-php-ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php protonemedia_php_ffmpeg
python3 parsarium.py run wav php protonemedia_php_ffmpeg controls/wav/256-samples.wav
python3 parsarium.py replay wav php protonemedia_php_ffmpeg CORPUS_DIR runs/wav-protonemedia_php_ffmpeg-replay
python3 parsarium.py afl build wav php protonemedia_php_ffmpeg
python3 parsarium.py afl prepare wav php protonemedia_php_ffmpeg runs/wav-protonemedia_php_ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
