# symfony/serializer — XML / PHP

Pinned release: `v8.1.11`. [Manifest](manifest.json) · [verification receipt](verification.json) · [AFL++ overlay receipt](../../../../fuzzing/afl-native/xml/php/symfony_serializer/verification.json)

[API, control result, and parser family](../../../../data/php/xml/symfony-serializer-parser.json)

## Run from the repository root

```sh
python3 parsarium.py build xml php symfony_serializer
python3 parsarium.py run xml php symfony_serializer controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php symfony_serializer CORPUS_DIR runs/xml-symfony_serializer-replay
python3 parsarium.py afl build xml php symfony_serializer
python3 parsarium.py afl prepare xml php symfony_serializer runs/xml-symfony_serializer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Xdebug line coverage sees only symfony/serializer PHP lines (XmlEncoder::decode and its DOM-to-array walk, plus the interfaces and trait it loads) and is reported separately. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 ext/dom/document.c, instrumented through an allowlist while the same XmlEncoder harness runs; libxml2 tree/XPath code, other ext/dom classes, ext/libxml and the interpreted XmlEncoder code add no AFL++ tuples, so the XmlEncoder lines that differ between the controls are visible only in the Xdebug report. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
