# boofcv-io — PNG / Java

Pinned release: `1.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/boofcv-io/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java boofcv_io
python3 parsarium.py run png java boofcv_io controls/png/red-green.png
python3 parsarium.py replay png java boofcv_io CORPUS_DIR runs/png-boofcv_io-replay
python3 parsarium.py afl build png java boofcv_io
python3 parsarium.py afl prepare png java boofcv_io runs/png-boofcv_io-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
