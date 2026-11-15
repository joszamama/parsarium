# pngmeta — PNG / Python

Pinned release: `0.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/pngmeta/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python pngmeta
python3 parsarium.py run png python pngmeta controls/png/red-green-title.png
python3 parsarium.py replay png python pngmeta CORPUS_DIR runs/png-pngmeta-replay
python3 parsarium.py afl build png python pngmeta
python3 parsarium.py afl prepare png python pngmeta runs/png-pngmeta-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
