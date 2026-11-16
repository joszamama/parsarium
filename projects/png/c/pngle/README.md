# pngle — PNG / C

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/pngle/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c pngle
python3 parsarium.py run png c pngle controls/png/red-green.png
python3 parsarium.py replay png c pngle CORPUS_DIR runs/png-pngle-replay
python3 parsarium.py afl build png c pngle
python3 parsarium.py afl prepare png c pngle runs/png-pngle-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
