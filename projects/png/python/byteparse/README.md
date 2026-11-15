# byteparse — PNG / Python

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/byteparse/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python byteparse
python3 parsarium.py run png python byteparse controls/png/red-green.png
python3 parsarium.py replay png python byteparse CORPUS_DIR runs/png-byteparse-replay
python3 parsarium.py afl build png python byteparse
python3 parsarium.py afl prepare png python byteparse runs/png-byteparse-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
