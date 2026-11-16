# jcodec — PNG / Java

Pinned release: `0.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/jcodec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java jcodec
python3 parsarium.py run png java jcodec controls/png/red-green.png
python3 parsarium.py replay png java jcodec CORPUS_DIR runs/png-jcodec-replay
python3 parsarium.py afl build png java jcodec
python3 parsarium.py afl prepare png java jcodec runs/png-jcodec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
