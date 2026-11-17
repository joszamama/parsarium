# php-dom — XML / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/xml/standard.json) · [AFL++ overlay receipt](../../../../fuzzing/afl-native/xml/php/stdlib_domdocument/verification.json)

`DOMDocument::loadXML()` on the control bytes as a string. PHP 8.5.12 (PHP License 3.01) and libxml2 2.15.4 (MIT) are built from pinned source archives. The overlay checks both `catalog-ns.xml` and `order-default-ns.xml` against the expat oracle and fuzzes `fuzz-target.php`, which only calls `loadXML`.

## Run from the repository root

```sh
python3 parsarium.py build xml php stdlib_domdocument
python3 parsarium.py run xml php stdlib_domdocument controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php stdlib_domdocument CORPUS_DIR runs/xml-stdlib_domdocument-replay
python3 parsarium.py afl build xml php stdlib_domdocument
python3 parsarium.py afl prepare xml php stdlib_domdocument runs/xml-stdlib_domdocument-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
