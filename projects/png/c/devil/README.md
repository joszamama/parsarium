# devil — PNG / C

Pinned release: `1.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/devil/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c devil
python3 parsarium.py run png c devil controls/png/red-green.png
python3 parsarium.py replay png c devil CORPUS_DIR runs/png-devil-replay
python3 parsarium.py afl build png c devil
python3 parsarium.py afl prepare png c devil runs/png-devil-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
