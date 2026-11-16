# arcana — ZIP / Java

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/arcana/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java arcana
python3 parsarium.py run zip java arcana controls/zip/hello.zip
python3 parsarium.py replay zip java arcana CORPUS_DIR runs/zip-arcana-replay
python3 parsarium.py afl build zip java arcana
python3 parsarium.py afl prepare zip java arcana runs/zip-arcana-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
