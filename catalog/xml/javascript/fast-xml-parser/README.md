# fast-xml-parser — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `5.12.1`
- **License:** MIT
- **Parser family:** fast-xml-parser own string scanner (OrderedObjParser + XMLValidator)
- **Local input API:** `new XMLParser({preserveOrder: true, ignoreAttributes: false, commentPropName: '#comment', trimValues: false, parseTagValue: false, htmlEntities: true}).parse(Buffer, true) on local bytes; the package decodes the Buffer with Buffer#toString and runs its own XMLValidator first. fast-xml-parser does no namespace processing, so the adapter resolves element and attribute prefixes from in-scope xmlns attributes and rejects unbound prefixes and duplicate expanded attributes`
- **Documentation:** [API reference](<https://github.com/NaturalIntelligence/fast-xml-parser/blob/v5.12.1/docs/v4%2C%20v5/2.XMLparseOptions.md>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/javascript/xml/parsers.json) · [control result](../../../../data/javascript/xml/verification.json)

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
python3 parsarium.py build xml javascript fast_xml_parser
python3 parsarium.py run xml javascript fast_xml_parser controls/xml/catalog-ns.xml
```
