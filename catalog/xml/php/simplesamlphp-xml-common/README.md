# simplesamlphp/xml-common — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v3.0.8`
- **Upstream:** [source repository](<https://github.com/simplesamlphp/xml-common>) · [Packagist](<https://packagist.org/packages/simplesamlphp/xml-common>)
- **License:** LGPL-2.1-or-later
- **Parser family:** libxml2 via PHP Dom\XMLDocument, shared with veewee/xml and the other libxml2 paths
- **Local input API:** `SimpleSAML\XML\DOMDocumentFactory::fromString(string $xml) with its default options (LIBXML_COMPACT | LIBXML_NONET | LIBXML_NSCLEAN | LIBXML_NO_XXE): rejects whitespace-only input and DOCTYPE markup, loads the string with Dom\XMLDocument::createFromString and returns the Dom\XMLDocument, walked namespace-aware`
- **Documentation:** [API reference](<https://github.com/simplesamlphp/xml-common/blob/c50b33dfc4384c772e921c6072bded9b67081c03/src/XML/DOMDocumentFactory.php>)
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
python3 parsarium.py build xml php simplesamlphp_xml_common
python3 parsarium.py run xml php simplesamlphp_xml_common controls/xml/catalog-ns.xml
```
