# zetacomponents/archive — ZIP / PHP

Pinned release: `1.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/zetacomponents-archive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php zetacomponents_archive
python3 parsarium.py run zip php zetacomponents_archive controls/zip/hello.zip
python3 parsarium.py replay zip php zetacomponents_archive CORPUS_DIR runs/zip-zetacomponents_archive-replay
python3 parsarium.py afl build zip php zetacomponents_archive
python3 parsarium.py afl prepare zip php zetacomponents_archive runs/zip-zetacomponents_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
