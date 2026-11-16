# music-tag — MP3 with ID3v2 / Python

Pinned release: `0.4.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/python/music-tag/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 python music_tag
python3 parsarium.py run mp3_id3v2 python music_tag controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 python music_tag CORPUS_DIR runs/mp3_id3v2-music_tag-replay
python3 parsarium.py afl build mp3_id3v2 python music_tag
python3 parsarium.py afl prepare mp3_id3v2 python music_tag runs/mp3_id3v2-music_tag-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
