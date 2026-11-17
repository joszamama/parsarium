# mpv — MP3 / C

Pinned release: `0.42.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/c/mpv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 c mpv
python3 parsarium.py run mp3_id3v2 c mpv controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 c mpv CORPUS_DIR runs/mp3_id3v2-mpv-replay
python3 parsarium.py afl build mp3_id3v2 c mpv
python3 parsarium.py afl prepare mp3_id3v2 c mpv runs/mp3_id3v2-mpv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
