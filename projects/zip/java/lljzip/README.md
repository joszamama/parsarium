# lljzip — ZIP / Java

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/lljzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java lljzip
python3 parsarium.py run zip java lljzip controls/zip/hello.zip
python3 parsarium.py replay zip java lljzip CORPUS_DIR runs/zip-lljzip-replay
python3 parsarium.py afl build zip java lljzip
python3 parsarium.py afl prepare zip java lljzip runs/zip-lljzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
