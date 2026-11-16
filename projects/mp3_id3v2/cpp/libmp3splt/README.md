# libmp3splt — MP3 with ID3v2 / C++

Pinned release: `0.9.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/cpp/libmp3splt/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 cpp libmp3splt
python3 parsarium.py run mp3_id3v2 cpp libmp3splt controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 cpp libmp3splt CORPUS_DIR runs/mp3_id3v2-libmp3splt-replay
python3 parsarium.py afl build mp3_id3v2 cpp libmp3splt
python3 parsarium.py afl prepare mp3_id3v2 cpp libmp3splt runs/mp3_id3v2-libmp3splt-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
