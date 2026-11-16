# decompress-unzip — ZIP / JavaScript

Pinned release: `4.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/decompress-unzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript decompress_unzip
python3 parsarium.py run zip javascript decompress_unzip controls/zip/hello.zip
python3 parsarium.py replay zip javascript decompress_unzip CORPUS_DIR runs/zip-decompress_unzip-replay
python3 parsarium.py afl build zip javascript decompress_unzip
python3 parsarium.py afl prepare zip javascript decompress_unzip runs/zip-decompress_unzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
