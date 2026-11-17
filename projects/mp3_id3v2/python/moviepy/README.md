# moviepy — MP3 / Python

Pinned release: `2.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/moviepy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 python moviepy
python3 parsarium.py run mp3_id3v2 python moviepy controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 python moviepy CORPUS_DIR runs/mp3_id3v2-moviepy-replay
python3 parsarium.py afl build mp3_id3v2 python moviepy
python3 parsarium.py afl prepare mp3_id3v2 python moviepy runs/mp3_id3v2-moviepy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
