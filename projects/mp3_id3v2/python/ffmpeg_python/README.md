# ffmpeg-python — MP3 with ID3v2 / Python

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/python/ffmpeg-python/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 python ffmpeg_python
python3 parsarium.py run mp3_id3v2 python ffmpeg_python controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 python ffmpeg_python CORPUS_DIR runs/mp3_id3v2-ffmpeg_python-replay
python3 parsarium.py afl build mp3_id3v2 python ffmpeg_python
python3 parsarium.py afl prepare mp3_id3v2 python ffmpeg_python runs/mp3_id3v2-ffmpeg_python-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
