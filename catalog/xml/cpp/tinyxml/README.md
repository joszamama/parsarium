# tinyxml — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.6.2`
- **License:** Zlib
- **Parser family:** TinyXML (version 1) own in-memory XML parser
- **Local input API:** `TiXmlDocument::Parse(const char* p, TiXmlParsingData* data = 0, TiXmlEncoding encoding) on a NUL-terminated copy of the local bytes with TIXML_ENCODING_UTF8, then TiXmlDocument::Error() and RootElement(); TinyXML does no namespace processing, so the adapter resolves prefixes from in-scope xmlns attributes`
- **Documentation:** [API reference](<https://www.grinninglizard.com/tinyxmldocs/classTiXmlDocument.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/cpp/xml/parsers.json) · [control result](../../../../data/cpp/xml/verification.json)

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
python3 parsarium.py build xml cpp tinyxml
python3 parsarium.py run xml cpp tinyxml controls/xml/catalog-ns.xml
```
