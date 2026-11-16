# jsmediatags — MP3 with ID3v2 / JavaScript

Pinned release: `3.9.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/javascript/jsmediatags/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript jsmediatags
python3 parsarium.py run mp3_id3v2 javascript jsmediatags controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript jsmediatags CORPUS_DIR runs/mp3_id3v2-jsmediatags-replay
python3 parsarium.py afl build mp3_id3v2 javascript jsmediatags
python3 parsarium.py afl prepare mp3_id3v2 javascript jsmediatags runs/mp3_id3v2-jsmediatags-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
