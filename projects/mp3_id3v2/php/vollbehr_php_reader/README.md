# vollbehr/php-reader — MP3 with ID3v2 / PHP

Pinned release: `v2.0-rc1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/php/vollbehr-php-reader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 php vollbehr_php_reader
python3 parsarium.py run mp3_id3v2 php vollbehr_php_reader controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 php vollbehr_php_reader CORPUS_DIR runs/mp3_id3v2-vollbehr_php_reader-replay
python3 parsarium.py afl build mp3_id3v2 php vollbehr_php_reader
python3 parsarium.py afl prepare mp3_id3v2 php vollbehr_php_reader runs/mp3_id3v2-vollbehr_php_reader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
