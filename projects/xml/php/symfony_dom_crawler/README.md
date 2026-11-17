# symfony/dom-crawler — XML / PHP

Pinned release: `v8.1.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/symfony-dom-crawler/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php symfony_dom_crawler
python3 parsarium.py run xml php symfony_dom_crawler controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php symfony_dom_crawler CORPUS_DIR runs/xml-symfony_dom_crawler-replay
python3 parsarium.py afl build xml php symfony_dom_crawler
python3 parsarium.py afl prepare xml php symfony_dom_crawler runs/xml-symfony_dom_crawler-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Xdebug line coverage sees only symfony/dom-crawler PHP lines (Crawler navigation, XPath relativizing and namespace discovery) and is reported separately. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 ext/dom/document.c and ext/libxml/libxml.c, instrumented through an allowlist while the same Crawler harness runs; libxml2 tree/XPath code, other ext/dom classes and the interpreted Crawler code add no AFL++ tuples. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
