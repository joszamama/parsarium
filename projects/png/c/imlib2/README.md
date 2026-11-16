# imlib2 — PNG / C

Pinned release: `1.12.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/imlib2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c imlib2
python3 parsarium.py run png c imlib2 controls/png/red-green.png
python3 parsarium.py replay png c imlib2 CORPUS_DIR runs/png-imlib2-replay
python3 parsarium.py afl build png c imlib2
python3 parsarium.py afl prepare png c imlib2 runs/png-imlib2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
