# imagecodecs — PNG / Python

Pinned release: `2026.10.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/imagecodecs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python imagecodecs
python3 parsarium.py run png python imagecodecs controls/png/red-green.png
python3 parsarium.py replay png python imagecodecs CORPUS_DIR runs/png-imagecodecs-replay
python3 parsarium.py afl build png python imagecodecs
python3 parsarium.py afl prepare png python imagecodecs runs/png-imagecodecs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
