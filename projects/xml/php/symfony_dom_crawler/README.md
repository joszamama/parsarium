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

**Coverage limit:** Xdebug and the AFL++ bridge see only symfony/dom-crawler PHP lines (Crawler navigation, XPath relativizing and namespace discovery); XML tokenizing happens in libxml2 through DOMDocument::loadXML and is not instrumented here. On the two shared controls the package line sets differ by one line (Crawler::findNamespacePrefixes no-prefix return).

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
