# symfony/dom-crawler — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v8.1.10`
- **License:** MIT
- **Parser family:** libxml2 via PHP DOMDocument, shared with the standard path and sabre/xml
- **Local input API:** `new Crawler() then Crawler::addXmlContent(string) (DOMDocument::loadXML with LIBXML_NONET always added); the XML-mode Crawler is traversed with children(), each(), nodeName(), attr(), text() and filterXPath() with namespace discovery and registerNamespace()`
- **Documentation:** [API reference](<https://symfony.com/doc/current/components/dom_crawler.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/php/xml/parsers.json) · [control result](../../../../data/php/xml/verification.json)

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

## Run this target

```sh
python3 parsarium.py build xml php symfony_dom_crawler
python3 parsarium.py run xml php symfony_dom_crawler controls/xml/catalog-ns.xml
```
