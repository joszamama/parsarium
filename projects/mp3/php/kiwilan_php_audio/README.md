# kiwilan/php-audio — MP3 / PHP

Pinned release: `4.0.02`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/php/kiwilan-php-audio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 php kiwilan_php_audio
python3 parsarium.py run mp3_id3v2 php kiwilan_php_audio controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 php kiwilan_php_audio CORPUS_DIR runs/mp3_id3v2-kiwilan_php_audio-replay
python3 parsarium.py afl build mp3_id3v2 php kiwilan_php_audio
python3 parsarium.py afl prepare mp3_id3v2 php kiwilan_php_audio runs/mp3_id3v2-kiwilan_php_audio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
