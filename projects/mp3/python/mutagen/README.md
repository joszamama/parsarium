# mutagen — MP3 / Python

Pinned release: `1.48.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/mutagen/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 python mutagen
python3 parsarium.py run mp3 python mutagen controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 python mutagen CORPUS_DIR runs/mp3-mutagen-replay
python3 parsarium.py afl build mp3 python mutagen
python3 parsarium.py afl prepare mp3 python mutagen runs/mp3-mutagen-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
