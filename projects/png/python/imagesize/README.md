# imagesize — PNG / Python

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/imagesize/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python imagesize
python3 parsarium.py run png python imagesize controls/png/red-green.png
python3 parsarium.py replay png python imagesize CORPUS_DIR runs/png-imagesize-replay
python3 parsarium.py afl build png python imagesize
python3 parsarium.py afl prepare png python imagesize runs/png-imagesize-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
