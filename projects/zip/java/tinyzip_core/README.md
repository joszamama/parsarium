# tinyzip-core — ZIP / Java

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/tinyzip-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java tinyzip_core
python3 parsarium.py run zip java tinyzip_core controls/zip/hello.zip
python3 parsarium.py replay zip java tinyzip_core CORPUS_DIR runs/zip-tinyzip_core-replay
python3 parsarium.py afl build zip java tinyzip_core
python3 parsarium.py afl prepare zip java tinyzip_core runs/zip-tinyzip_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
