# christophwurst/id3parser — MP3 / PHP

Pinned release: `v0.1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/php/christophwurst-id3parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 php christophwurst_id3parser
python3 parsarium.py run mp3_id3v2 php christophwurst_id3parser controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 php christophwurst_id3parser CORPUS_DIR runs/mp3_id3v2-christophwurst_id3parser-replay
python3 parsarium.py afl build mp3_id3v2 php christophwurst_id3parser
python3 parsarium.py afl prepare mp3_id3v2 php christophwurst_id3parser runs/mp3_id3v2-christophwurst_id3parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
