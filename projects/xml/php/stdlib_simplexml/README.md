# php-simplexml — XML / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/xml/standard.json) · [AFL++ overlay receipt](../../../../fuzzing/afl-native/xml/php/stdlib_simplexml/verification.json)

`simplexml_load_string()` on the control bytes as a string. PHP 8.5.12 (PHP License 3.01, built with `--enable-simplexml`) and libxml2 2.15.4 (MIT) are built from pinned source archives; `ext/simplexml/simplexml.c` and `php_simplexml.h` are also pinned by SHA-256. The overlay checks both `catalog-ns.xml` and `order-default-ns.xml` against the expat oracle and fuzzes `fuzz-target.php`, which only calls `simplexml_load_string`.

SimpleXML has no text-node accessor: an element's string value joins its direct text and CDATA, so text split by child elements, comments or PIs inside one element is merged. Comments, PIs and the XML declaration are not exposed. Neither control has such mixed content.

## Run from the repository root

```sh
python3 parsarium.py build xml php stdlib_simplexml
python3 parsarium.py run xml php stdlib_simplexml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php stdlib_simplexml CORPUS_DIR runs/xml-stdlib_simplexml-replay
python3 parsarium.py afl build xml php stdlib_simplexml
python3 parsarium.py afl prepare xml php stdlib_simplexml runs/xml-stdlib_simplexml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
