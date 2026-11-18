# saloonphp/xml-wrangler — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.5.0`
- **Upstream:** [source repository](<https://github.com/saloonphp/xml-wrangler>) · [Packagist](<https://packagist.org/packages/saloonphp/xml-wrangler>)
- **License:** MIT
- **Parser family:** libxml2 via PHP XMLReader and DOMDocument, shared with the standard path, sabre/xml and symfony/dom-crawler
- **Local input API:** `XmlReader::fromString(string) then elements() (documented; returns Element DTOs keyed by element name); fromFile(path) and fromStream(resource) are cross-checked for the same summary`
- **Documentation:** [API reference](<https://github.com/saloonphp/xml-wrangler/blob/4f35b68245dee8041193369efd4d73a98ad04a5f/.github/README.md>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/php/xml/parsers.json) · [control result](../../../../data/php/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "version=1",
    "id=a1",
    "c:lang=es",
    "id=b2"
  ],
  "elements": [
    "c:catalog",
    "item",
    "item",
    "name",
    "note"
  ],
  "leaf_text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ],
  "max_depth": 3,
  "namespace_declarations": [
    "c:catalog xmlns=urn:parsarium:item",
    "c:catalog xmlns:c=urn:parsarium:catalog"
  ],
  "root": "c:catalog"
}
```

## Run this target

```sh
python3 parsarium.py build xml php saloon_xml_wrangler
python3 parsarium.py run xml php saloon_xml_wrangler controls/xml/catalog-ns.xml
```
