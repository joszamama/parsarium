# mhor/php-mediainfo — MP4 / PHP

Pinned release: `5.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/mhor-php-mediainfo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php mhor_php_mediainfo
python3 parsarium.py run mp4 php mhor_php_mediainfo controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php mhor_php_mediainfo CORPUS_DIR runs/mp4-mhor_php_mediainfo-replay
python3 parsarium.py afl build mp4 php mhor_php_mediainfo
python3 parsarium.py afl prepare mp4 php mhor_php_mediainfo runs/mp4-mhor_php_mediainfo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
