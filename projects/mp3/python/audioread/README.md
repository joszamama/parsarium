# audioread — MP3 / Python

Pinned release: `3.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/audioread/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 python audioread
python3 parsarium.py run mp3 python audioread controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 python audioread CORPUS_DIR runs/mp3-audioread-replay
python3 parsarium.py afl build mp3 python audioread
python3 parsarium.py afl prepare mp3 python audioread runs/mp3-audioread-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
