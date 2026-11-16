# comodojo/zip — ZIP / PHP

Pinned release: `3.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/comodojo-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php comodojo_zip
python3 parsarium.py run zip php comodojo_zip controls/zip/hello.zip
python3 parsarium.py replay zip php comodojo_zip CORPUS_DIR runs/zip-comodojo_zip-replay
python3 parsarium.py afl build zip php comodojo_zip
python3 parsarium.py afl prepare zip php comodojo_zip runs/zip-comodojo_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
