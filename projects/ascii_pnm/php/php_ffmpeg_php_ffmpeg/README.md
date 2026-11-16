# php-ffmpeg/php-ffmpeg — ASCII PNM / PHP

Pinned release: `v1.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/php-ffmpeg-php-ffmpeg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php php_ffmpeg_php_ffmpeg
python3 parsarium.py run ascii_pnm php php_ffmpeg_php_ffmpeg controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php php_ffmpeg_php_ffmpeg CORPUS_DIR runs/ascii_pnm-php_ffmpeg_php_ffmpeg-replay
python3 parsarium.py afl build ascii_pnm php php_ffmpeg_php_ffmpeg
python3 parsarium.py afl prepare ascii_pnm php php_ffmpeg_php_ffmpeg runs/ascii_pnm-php_ffmpeg_php_ffmpeg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
