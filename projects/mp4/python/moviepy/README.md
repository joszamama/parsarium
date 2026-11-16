# moviepy — MP4 / Python

Pinned release: `2.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/python/moviepy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 python moviepy
python3 parsarium.py run mp4 python moviepy controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 python moviepy CORPUS_DIR runs/mp4-moviepy-replay
python3 parsarium.py afl build mp4 python moviepy
python3 parsarium.py afl prepare mp4 python moviepy runs/mp4-moviepy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
