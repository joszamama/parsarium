# vipsoft/unzip — ZIP / PHP

Pinned release: `1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/vipsoft-unzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php vipsoft_unzip
python3 parsarium.py run zip php vipsoft_unzip controls/zip/hello.zip
python3 parsarium.py replay zip php vipsoft_unzip CORPUS_DIR runs/zip-vipsoft_unzip-replay
python3 parsarium.py afl build zip php vipsoft_unzip
python3 parsarium.py afl prepare zip php vipsoft_unzip runs/zip-vipsoft_unzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
