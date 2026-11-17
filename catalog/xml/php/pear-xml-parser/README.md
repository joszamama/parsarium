# pear/xml_parser — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.3.8`
- **License:** BSD-2-Clause
- **Parser family:** libxml2 push parser via PHP ext/xml (xml_parser_create/xml_parse through ext/xml/compat.c); shared with the standard xml_parser_create_ns/xml_parse path and the other libxml2 package paths
- **Local input API:** `new XML_Parser(), setHandlerObj(handler), setInputString(string) then parse() (documented in the PEAR manual 'Choosing input'); setInputFile(path) and setInput(resource) are cross-checked for the same summary`
- **Documentation:** [API reference](<https://pear.php.net/manual/en/package.xml.xml-parser.input.php>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/php/xml/parsers.json) · [control result](../../../../data/php/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "xmlns:c=urn:parsarium:catalog",
    "xmlns=urn:parsarium:item",
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
  "max_depth": 3,
  "processing_instructions": [],
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
python3 parsarium.py build xml php pear_xml_parser
python3 parsarium.py run xml php pear_xml_parser controls/xml/catalog-ns.xml
```
