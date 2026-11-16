# decompress-zip — ZIP / JavaScript

Pinned release: `0.3.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/decompress-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript decompress_zip
python3 parsarium.py run zip javascript decompress_zip controls/zip/hello.zip
python3 parsarium.py replay zip javascript decompress_zip CORPUS_DIR runs/zip-decompress_zip-replay
python3 parsarium.py afl build zip javascript decompress_zip
python3 parsarium.py afl prepare zip javascript decompress_zip runs/zip-decompress_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
