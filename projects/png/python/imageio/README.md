# imageio — PNG / Python

Pinned release: `2.38.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/imageio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python imageio
python3 parsarium.py run png python imageio controls/png/red-green.png
python3 parsarium.py replay png python imageio CORPUS_DIR runs/png-imageio-replay
python3 parsarium.py afl build png python imageio
python3 parsarium.py afl prepare png python imageio runs/png-imageio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
