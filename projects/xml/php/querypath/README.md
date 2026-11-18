# querypath/querypath — XML / PHP

Pinned release: `3.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/querypath-querypath/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php querypath
python3 parsarium.py run xml php querypath controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php querypath CORPUS_DIR runs/xml-querypath-replay
python3 parsarium.py afl build xml php querypath
python3 parsarium.py afl prepare xml php querypath runs/xml-querypath-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Xdebug line coverage sees only querypath/querypath PHP lines and is reported separately. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 ext/dom/document.c, instrumented through an allowlist while the same harness runs; libxml2 tree/XPath code, other ext/dom classes, ext/libxml and the interpreted querypath/querypath code add no AFL++ tuples. querypath/querypath is a loader over DOMDocument::loadXML (libxml2 family, shared with the standard DOMDocument path, symfony/dom-crawler, symfony/serializer and mtownsend/xml-to-array); its own lines are visible only in the Xdebug report. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
