# lame — MP3 / C++

Pinned release: `4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/cpp/lame/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 cpp lame
python3 parsarium.py run mp3_id3v2 cpp lame controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 cpp lame CORPUS_DIR runs/mp3_id3v2-lame-replay
python3 parsarium.py afl build mp3_id3v2 cpp lame
python3 parsarium.py afl prepare mp3_id3v2 cpp lame runs/mp3_id3v2-lame-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
