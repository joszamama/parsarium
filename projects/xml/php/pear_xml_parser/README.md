# pear/xml_parser — XML / PHP

Pinned release: `v1.3.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/pear-xml-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php pear_xml_parser
python3 parsarium.py run xml php pear_xml_parser controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php pear_xml_parser CORPUS_DIR runs/xml-pear_xml_parser-replay
python3 parsarium.py afl build xml php pear_xml_parser
python3 parsarium.py afl prepare xml php pear_xml_parser runs/xml-pear_xml_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** One run records two line-coverage sources for the documented setInputString()/parse() call: Xdebug 3.5.3 executed lines in pear/xml_parser PHP source (XML/Parser.php; the Xdebug pseudo-line past the end of each first-loaded class file is removed) and Clang/LLVM source coverage of PHP 8.5.12 ext/xml (xml.c, compat.c) and source-built libxml2 2.15.4. The setInputFile()/setInput() cross-check runs in a separate process and is not counted. The package PHP lines are the same on both controls: XML_Parser dispatches every SAX event from ext/xml's C callbacks to the handler object, so its own code path does not depend on the document. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 ext/xml/xml.c and ext/xml/compat.c, instrumented through an allowlist while the same harness runs; the interpreted XML_Parser and PEAR code, ext/libxml/libxml.c, libxml2 tree/XPath/dict code and the Zend engine add no AFL++ tuples. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
