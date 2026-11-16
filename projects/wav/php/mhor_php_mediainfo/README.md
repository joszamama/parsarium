# mhor/php-mediainfo — WAV / PHP

Pinned release: `5.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/mhor-php-mediainfo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php mhor_php_mediainfo
python3 parsarium.py run wav php mhor_php_mediainfo controls/wav/32768-samples.wav
python3 parsarium.py replay wav php mhor_php_mediainfo CORPUS_DIR runs/wav-mhor_php_mediainfo-replay
python3 parsarium.py afl build wav php mhor_php_mediainfo
python3 parsarium.py afl prepare wav php mhor_php_mediainfo runs/wav-mhor_php_mediainfo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
