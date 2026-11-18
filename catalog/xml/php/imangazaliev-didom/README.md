# imangazaliev/didom — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.0.1`
- **License:** MIT
- **Parser family:** libxml2 via PHP DOMDocument, shared with the standard path, symfony/dom-crawler, symfony/serializer and mtownsend/xml-to-array
- **Local input API:** `new DiDom\Document(string $xml, false, 'UTF-8', Document::TYPE_XML) on the local bytes (the constructor sets preserveWhiteSpace = false; Document::load trims the string and calls DOMDocument::loadXML with LIBXML_HTML_NODEFDTD); Document::getDocument() returns that DOMDocument, walked namespace-aware`
- **Documentation:** [API reference](<https://github.com/Imangazaliev/DiDOM/blob/50fa6595d14f22c0c984efed5c818485cf548136/README.md>)
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
python3 parsarium.py build xml php didom
python3 parsarium.py run xml php didom controls/xml/catalog-ns.xml
```
