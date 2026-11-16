# id3-reader — MP3 with ID3v2 / JavaScript

Pinned release: `0.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/javascript/id3-reader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript id3_reader
python3 parsarium.py run mp3_id3v2 javascript id3_reader controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript id3_reader CORPUS_DIR runs/mp3_id3v2-id3_reader-replay
python3 parsarium.py afl build mp3_id3v2 javascript id3_reader
python3 parsarium.py afl prepare mp3_id3v2 javascript id3_reader runs/mp3_id3v2-id3_reader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
