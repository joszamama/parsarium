# tinytag — MP3 / Python

Pinned release: `2.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/tinytag/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 python tinytag
python3 parsarium.py run mp3_id3v2 python tinytag controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 python tinytag CORPUS_DIR runs/mp3_id3v2-tinytag-replay
python3 parsarium.py afl build mp3_id3v2 python tinytag
python3 parsarium.py afl prepare mp3_id3v2 python tinytag runs/mp3_id3v2-tinytag-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
