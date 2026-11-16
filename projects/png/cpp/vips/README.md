# vips — PNG / C++

Pinned release: `8.18.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp vips
python3 parsarium.py run png cpp vips controls/png/red-green.png
python3 parsarium.py replay png cpp vips CORPUS_DIR runs/png-vips-replay
python3 parsarium.py afl build png cpp vips
python3 parsarium.py afl prepare png cpp vips runs/png-vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
