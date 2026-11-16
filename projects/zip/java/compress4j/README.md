# compress4j — ZIP / Java

Pinned release: `5.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/compress4j/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java compress4j
python3 parsarium.py run zip java compress4j controls/zip/hello.zip
python3 parsarium.py replay zip java compress4j CORPUS_DIR runs/zip-compress4j-replay
python3 parsarium.py afl build zip java compress4j
python3 parsarium.py afl prepare zip java compress4j runs/zip-compress4j-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
