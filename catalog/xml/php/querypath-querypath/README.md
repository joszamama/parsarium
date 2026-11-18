# querypath/querypath — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.0.5`
- **Upstream:** [source repository](<https://github.com/technosophos/querypath>) · [Packagist](<https://packagist.org/packages/querypath/querypath>)
- **License:** MIT
- **Parser family:** libxml2 via PHP DOMDocument, shared with the standard path, symfony/dom-crawler, symfony/serializer and mtownsend/xml-to-array
- **Local input API:** `qp(string $xml) (QueryPath::with) on the local bytes, which DOMQuery::parseXMLString loads with DOMDocument::loadXML because the string starts with an XML declaration; DOMQuery::document() returns that DOMDocument, walked namespace-aware`
- **Documentation:** [API reference](<https://github.com/technosophos/querypath/blob/6b8e2395fac61fac25bbe962f94def556cb85f7d/README.md>)
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
  "namespace_declarations": 2,
  "namespaces": [
    "urn:parsarium:catalog",
    "urn:parsarium:item"
  ],
  "root": "{urn:parsarium:catalog}catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml php querypath
python3 parsarium.py run xml php querypath controls/xml/catalog-ns.xml
```
