# wikimedia/getid3 — MP3 with ID3v2 / PHP

Pinned release: `v2.0.0-beta5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/php/wikimedia-getid3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 php wikimedia_getid3
python3 parsarium.py run mp3_id3v2 php wikimedia_getid3 controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 php wikimedia_getid3 CORPUS_DIR runs/mp3_id3v2-wikimedia_getid3-replay
python3 parsarium.py afl build mp3_id3v2 php wikimedia_getid3
python3 parsarium.py afl prepare mp3_id3v2 php wikimedia_getid3 runs/mp3_id3v2-wikimedia_getid3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
