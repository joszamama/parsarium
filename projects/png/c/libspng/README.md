# libspng — PNG / C

Pinned release: `0.7.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/libspng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c libspng
python3 parsarium.py run png c libspng controls/png/red-green.png
python3 parsarium.py replay png c libspng CORPUS_DIR runs/png-libspng-replay
python3 parsarium.py afl build png c libspng
python3 parsarium.py afl prepare png c libspng runs/png-libspng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
