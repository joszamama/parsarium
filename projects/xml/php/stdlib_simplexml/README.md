# php-simplexml — XML / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/xml/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build xml php stdlib_simplexml
python3 parsarium.py run xml php stdlib_simplexml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php stdlib_simplexml CORPUS_DIR runs/xml-stdlib_simplexml-replay
python3 parsarium.py afl build xml php stdlib_simplexml
python3 parsarium.py afl prepare xml php stdlib_simplexml runs/xml-stdlib_simplexml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
