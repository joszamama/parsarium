# mmoreram/extractor — ZIP / PHP

Pinned release: `1.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/mmoreram-extractor/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php mmoreram_extractor
python3 parsarium.py run zip php mmoreram_extractor controls/zip/hello.zip
python3 parsarium.py replay zip php mmoreram_extractor CORPUS_DIR runs/zip-mmoreram_extractor-replay
python3 parsarium.py afl build zip php mmoreram_extractor
python3 parsarium.py afl prepare zip php mmoreram_extractor runs/zip-mmoreram_extractor-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
