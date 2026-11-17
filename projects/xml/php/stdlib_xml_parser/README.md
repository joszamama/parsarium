# php-xml — XML / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/xml/standard.json) · [AFL++ overlay receipt](../../../../fuzzing/afl-native/xml/php/stdlib_xml_parser/verification.json)

`xml_parser_create_ns()` plus `xml_parse()` on the control bytes, in one final chunk. This is PHP's XML Parser extension (`ext/xml`): without `--with-expat` it runs libxml2's push parser (`xmlCreatePushParserCtxt`, `xmlParseChunk`) through `ext/xml/compat.c`, an expat-compatible SAX layer, and builds no tree. The summary is collected in the PHP event handlers while `xml_parse` runs. PHP 8.5.12 (PHP License 3.01, built with `--enable-xml`) and libxml2 2.15.4 (MIT) are built from pinned source archives; `ext/xml/xml.c`, `compat.c`, `expat_compat.h` and `php_xml.h` are also pinned by SHA-256. The overlay checks both `catalog-ns.xml` and `order-default-ns.xml` against the expat oracle and fuzzes `fuzz-target.php`, which runs the same handlers without the JSON output.

Case folding, which `ext/xml` turns on by default, is turned off. The namespace separator is `"\x01"`, which can't appear in a URI or anywhere in well-formed XML 1.0; `ext/xml` only uses the first byte of the separator. CDATA and character data both arrive through the character data handler. `ext/xml` has no comment handler, so comments reach the default handler and only mark a text boundary. Any other default-handler data, such as an unexpanded user-defined entity reference (which needs a DTD), makes the harness fail instead of producing a summary. Chunked feeding and `xml_parse_into_struct` aren't exercised.

## Run from the repository root

```sh
python3 parsarium.py build xml php stdlib_xml_parser
python3 parsarium.py run xml php stdlib_xml_parser controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php stdlib_xml_parser CORPUS_DIR runs/xml-stdlib_xml_parser-replay
python3 parsarium.py afl build xml php stdlib_xml_parser
python3 parsarium.py afl prepare xml php stdlib_xml_parser runs/xml-stdlib_xml_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
