# zip4j — ZIP / Java

Pinned release: `2.11.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/zip4j/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java zip4j
python3 parsarium.py run zip java zip4j controls/zip/hello.zip
python3 parsarium.py replay zip java zip4j CORPUS_DIR runs/zip-zip4j-replay
python3 parsarium.py afl build zip java zip4j
python3 parsarium.py afl prepare zip java zip4j runs/zip-zip4j-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
