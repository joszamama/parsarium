# smuuf/zip-reader — ZIP / PHP

Pinned release: `1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/smuuf-zip-reader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php smuuf_zip_reader
python3 parsarium.py run zip php smuuf_zip_reader controls/zip/hello.zip
python3 parsarium.py replay zip php smuuf_zip_reader CORPUS_DIR runs/zip-smuuf_zip_reader-replay
python3 parsarium.py afl build zip php smuuf_zip_reader
python3 parsarium.py afl prepare zip php smuuf_zip_reader runs/zip-smuuf_zip_reader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
