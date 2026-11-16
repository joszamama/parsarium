# @xhmikosr/decompress-unzip — ZIP / JavaScript

Pinned release: `8.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/xhmikosr-decompress-unzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript xhmikosr_decompress_unzip
python3 parsarium.py run zip javascript xhmikosr_decompress_unzip controls/zip/hello.zip
python3 parsarium.py replay zip javascript xhmikosr_decompress_unzip CORPUS_DIR runs/zip-xhmikosr_decompress_unzip-replay
python3 parsarium.py afl build zip javascript xhmikosr_decompress_unzip
python3 parsarium.py afl prepare zip javascript xhmikosr_decompress_unzip runs/zip-xhmikosr_decompress_unzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
