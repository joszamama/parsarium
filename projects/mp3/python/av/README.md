# av — MP3 / Python

Pinned release: `19.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/av/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 python av
python3 parsarium.py run mp3_id3v2 python av controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 python av CORPUS_DIR runs/mp3_id3v2-av-replay
python3 parsarium.py afl build mp3_id3v2 python av
python3 parsarium.py afl prepare mp3_id3v2 python av runs/mp3_id3v2-av-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
