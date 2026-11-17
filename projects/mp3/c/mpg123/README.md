# mpg123 — MP3 / C

Pinned release: `1.33.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/c/mpg123/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 c mpg123
python3 parsarium.py run mp3 c mpg123 controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 c mpg123 CORPUS_DIR runs/mp3-mpg123-replay
python3 parsarium.py afl build mp3 c mpg123
python3 parsarium.py afl prepare mp3 c mpg123 runs/mp3-mpg123-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
