# pymediainfo — MP4 / Python

Pinned release: `7.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/python/pymediainfo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 python pymediainfo
python3 parsarium.py run mp4 python pymediainfo controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 python pymediainfo CORPUS_DIR runs/mp4-pymediainfo-replay
python3 parsarium.py afl build mp4 python pymediainfo
python3 parsarium.py afl prepare mp4 python pymediainfo runs/mp4-pymediainfo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
