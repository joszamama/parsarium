# devil — PNG / C++

Pinned release: `1.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/devil/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp devil
python3 parsarium.py run png cpp devil controls/png/red-green.png
python3 parsarium.py replay png cpp devil CORPUS_DIR runs/png-devil-replay
python3 parsarium.py afl build png cpp devil
python3 parsarium.py afl prepare png cpp devil runs/png-devil-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
