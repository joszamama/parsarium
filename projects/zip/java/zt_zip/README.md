# zt-zip — ZIP / Java

Pinned release: `1.18.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/zt-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java zt_zip
python3 parsarium.py run zip java zt_zip controls/zip/hello.zip
python3 parsarium.py replay zip java zt_zip CORPUS_DIR runs/zip-zt_zip-replay
python3 parsarium.py afl build zip java zt_zip
python3 parsarium.py afl prepare zip java zt_zip runs/zip-zt_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
