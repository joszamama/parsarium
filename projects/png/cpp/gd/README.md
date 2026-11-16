# gd — PNG / C++

Pinned release: `2.3.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/gd/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp gd
python3 parsarium.py run png cpp gd controls/png/red-green.png
python3 parsarium.py replay png cpp gd CORPUS_DIR runs/png-gd-replay
python3 parsarium.py afl build png cpp gd
python3 parsarium.py afl prepare png cpp gd runs/png-gd-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
