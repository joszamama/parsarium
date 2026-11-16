# pngle — PNG / C++

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/pngle/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp pngle
python3 parsarium.py run png cpp pngle controls/png/red-green.png
python3 parsarium.py replay png cpp pngle CORPUS_DIR runs/png-pngle-replay
python3 parsarium.py afl build png cpp pngle
python3 parsarium.py afl prepare png cpp pngle runs/png-pngle-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
