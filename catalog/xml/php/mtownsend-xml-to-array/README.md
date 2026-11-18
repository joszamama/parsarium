# mtownsend/xml-to-array — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.0.1`
- **Upstream:** [source repository](<https://github.com/mtownsend5512/xml-to-array>) · [Packagist](<https://packagist.org/packages/mtownsend/xml-to-array>)
- **License:** MIT
- **Parser family:** libxml2 via PHP DOMDocument, shared with the standard path, symfony/dom-crawler and symfony/serializer
- **Local input API:** `XmlToArray::convert(string $xml, bool $outputRoot = false) (the README's documented entry point; the global xml_to_array() helper forwards to it), called with $outputRoot = true. It loads the string with DOMDocument::loadXML and default options, then walks the DOM from documentElement into a PHP array; '@root' holds the root tagName`
- **Documentation:** [API reference](<https://github.com/mtownsend5512/xml-to-array/blob/8e4b08ae0f56f1e2a77b4b88a0e17bce0200350e/README.md>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/php/xml/parsers.json) · [control result](../../../../data/php/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "version=1",
    "id=a1",
    "lang=es",
    "id=b2"
  ],
  "elements": [
    "item",
    "item",
    "name",
    "note"
  ],
  "max_depth": 3,
  "root": "c:catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml php mtownsend_xml_to_array
python3 parsarium.py run xml php mtownsend_xml_to_array controls/xml/catalog-ns.xml
```
