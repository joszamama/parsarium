# itext-io — PNG / Java

Pinned release: `9.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/itext-io/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java itext_io
python3 parsarium.py run png java itext_io controls/png/red-green.png
python3 parsarium.py replay png java itext_io CORPUS_DIR runs/png-itext_io-replay
python3 parsarium.py afl build png java itext_io
python3 parsarium.py afl prepare png java itext_io runs/png-itext_io-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
