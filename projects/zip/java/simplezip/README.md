# simplezip — ZIP / Java

Pinned release: `2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/simplezip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java simplezip
python3 parsarium.py run zip java simplezip controls/zip/hello.zip
python3 parsarium.py replay zip java simplezip CORPUS_DIR runs/zip-simplezip-replay
python3 parsarium.py afl build zip java simplezip
python3 parsarium.py afl prepare zip java simplezip runs/zip-simplezip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
