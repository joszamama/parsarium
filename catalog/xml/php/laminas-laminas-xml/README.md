# laminas/laminas-xml — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.8.0`
- **Upstream:** [source repository](<https://github.com/laminas/laminas-xml>) · [Packagist](<https://packagist.org/packages/laminas/laminas-xml>)
- **License:** BSD-3-Clause
- **Parser family:** libxml2 via PHP DOMDocument, shared with the standard path, symfony/dom-crawler, symfony/serializer and mtownsend/xml-to-array
- **Local input API:** `Laminas\Xml\Security::scan(string $xml, DOMDocument $dom) on the local bytes: DOMDocument::loadXML with LIBXML_NONET and internal libxml errors, a post-parse check that no DOCTYPE declares entities (the string heuristic runs only under PHP-FPM, not in this CLI harness), and the loaded DOMDocument returned (SimpleXMLElement when no DOMDocument is passed); walked namespace-aware`
- **Documentation:** [API reference](<https://docs.laminas.dev/laminas-xml/>)
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
python3 parsarium.py build xml php laminas_xml
python3 parsarium.py run xml php laminas_xml controls/xml/catalog-ns.xml
```
