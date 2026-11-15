# hachoir — MP4 / Python

Pinned release: `3.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/python/hachoir/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 python hachoir
python3 parsarium.py run mp4 python hachoir controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 python hachoir CORPUS_DIR runs/mp4-hachoir-replay
python3 parsarium.py afl build mp4 python hachoir
python3 parsarium.py afl prepare mp4 python hachoir runs/mp4-hachoir-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
