# audioread — MP4 / Python

Pinned release: `3.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/python/audioread/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 python audioread
python3 parsarium.py run mp4 python audioread controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 python audioread CORPUS_DIR runs/mp4-audioread-replay
python3 parsarium.py afl build mp4 python audioread
python3 parsarium.py afl prepare mp4 python audioread runs/mp4-audioread-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
