# imageio — MP4 / Python

Pinned release: `2.38.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/python/imageio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 python imageio
python3 parsarium.py run mp4 python imageio controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 python imageio CORPUS_DIR runs/mp4-imageio-replay
python3 parsarium.py afl build mp4 python imageio
python3 parsarium.py afl prepare mp4 python imageio runs/mp4-imageio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
