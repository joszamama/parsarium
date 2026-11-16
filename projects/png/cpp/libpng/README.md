# libpng — PNG / C++

Pinned release: `1.6.59`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/libpng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp libpng
python3 parsarium.py run png cpp libpng controls/png/red-green.png
python3 parsarium.py replay png cpp libpng CORPUS_DIR runs/png-libpng-replay
python3 parsarium.py afl build png cpp libpng
python3 parsarium.py afl prepare png cpp libpng runs/png-libpng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
