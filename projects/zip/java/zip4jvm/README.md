# zip4jvm — ZIP / Java

Pinned release: `1.13`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/zip4jvm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java zip4jvm
python3 parsarium.py run zip java zip4jvm controls/zip/hello.zip
python3 parsarium.py replay zip java zip4jvm CORPUS_DIR runs/zip-zip4jvm-replay
python3 parsarium.py afl build zip java zip4jvm
python3 parsarium.py afl prepare zip java zip4jvm runs/zip-zip4jvm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
