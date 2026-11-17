# symfony/dom-crawler — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v8.1.10`
- **License:** MIT
- **Parser family:** libxml2 via PHP DOMDocument, shared with the standard path and sabre/xml
- **Local input API:** `new Crawler() then Crawler::addXmlContent(string) (DOMDocument::loadXML with LIBXML_NONET always added); the XML-mode Crawler is traversed with children(), each(), nodeName(), attr(), text() and filterXPath() with namespace discovery and registerNamespace()`
- **Package-own scope:** Crawler XML-mode navigation and query mapping: the addXmlContent default-namespace rewrite check, children()/sibling() element traversal, attr()/text() whitespace normalizing, filterXPath() relativizing, findNamespacePrefixes() and discoverNamespace(). Tokenizing, well-formedness, entity decoding and namespace binding are libxml2.
- **Documentation:** [API reference](<https://symfony.com/doc/current/components/dom_crawler.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml); second control [`controls/xml/order-default-ns.xml`](../../../../controls/xml/order-default-ns.xml)
- **Adoption:** 443,886,072 cumulative Packagist downloads (captured 2026-11-17). Most of them are HTML crawling and functional-test uses, not XML parsing.
- **Catalog evidence:** [parser record](../../../../data/php/xml/parsers.json) · [control result](../../../../data/php/xml/verification.json) · [AFL++ feedback](../../../../data/php/xml/afl-feedback.json)

## Observed control result

```json
{
  "attributes": [
    "version=1",
    "id=a1",
    "{urn:parsarium:catalog}lang=es",
    "id=b2"
  ],
  "elements": [
    "{urn:parsarium:catalog}catalog",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}name",
    "{urn:parsarium:item}note"
  ],
  "max_depth": 3,
  "root": "{urn:parsarium:catalog}catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ],
  "xpath": {
    "//c:catalog": 1,
    "//ns1:item": 2,
    "//ns1:name": 1,
    "//ns1:note": 1
  }
}
```

## Limits

- Crawler's documented default-namespace prefix ('default') resolves to the last default namespace declaration in the document; the order control's <plain xmlns=""> leaves it unbound, so the harness registers default-namespace URIs as ns1, ns2, ... with registerNamespace() and keeps auto-discovery for prefixed names.
- addXmlContent replaces every 'xmlns' with 'ns' when the text has no 'xmlns:' prefix declaration; both shared controls declare a prefix, so that rewrite is not exercised.
- addXmlContent suppresses libxml errors and yields an empty Crawler for non-well-formed text; only valid controls were run.
- Coverage and AFL++ feedback come from symfony/dom-crawler PHP lines only. On the two controls they differ by one package line (`Crawler::findNamespacePrefixes` returning no prefixes for the order control's unqualified elements); libxml2 tokenizing is not instrumented in this path.

## Run this target

```sh
python3 parsarium.py build xml php symfony_dom_crawler
python3 parsarium.py run xml php symfony_dom_crawler controls/xml/catalog-ns.xml
```
