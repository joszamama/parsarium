# nelexa/zip — ZIP / PHP

Pinned release: `4.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/nelexa-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php nelexa_zip
python3 parsarium.py run zip php nelexa_zip controls/zip/hello.zip
python3 parsarium.py replay zip php nelexa_zip CORPUS_DIR runs/zip-nelexa_zip-replay
python3 parsarium.py afl build zip php nelexa_zip
python3 parsarium.py afl prepare zip php nelexa_zip runs/zip-nelexa_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
