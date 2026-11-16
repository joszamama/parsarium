# commons-archive — ZIP / Java

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/commons-archive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java commons_archive
python3 parsarium.py run zip java commons_archive controls/zip/hello.zip
python3 parsarium.py replay zip java commons_archive CORPUS_DIR runs/zip-commons_archive-replay
python3 parsarium.py afl build zip java commons_archive
python3 parsarium.py afl prepare zip java commons_archive runs/zip-commons_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
