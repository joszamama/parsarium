# wapmorgan/media-file — MP3 / PHP

Pinned release: `0.1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/php/wapmorgan-media-file/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 php wapmorgan_media_file
python3 parsarium.py run mp3 php wapmorgan_media_file controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 php wapmorgan_media_file CORPUS_DIR runs/mp3-wapmorgan_media_file-replay
python3 parsarium.py afl build mp3 php wapmorgan_media_file
python3 parsarium.py afl prepare mp3 php wapmorgan_media_file runs/mp3-wapmorgan_media_file-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
