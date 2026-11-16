# audiomath — MP4 / Python

Pinned release: `1.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/python/audiomath/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 python audiomath
python3 parsarium.py run mp4 python audiomath controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 python audiomath CORPUS_DIR runs/mp4-audiomath-replay
python3 parsarium.py afl build mp4 python audiomath
python3 parsarium.py afl prepare mp4 python audiomath runs/mp4-audiomath-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
