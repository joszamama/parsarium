# libxml++ — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `5.6.1`
- **License:** LGPL-2.1-or-later
- **Parser family:** libxml2 XML parser (shared underlying C parser)
- **Local input API:** `xmlpp::DomParser::parse_memory_raw(const unsigned char*, size_type) on an in-memory local byte buffer; namespace-aware DOM via libxml2`
- **Documentation:** [API reference](<https://github.com/libxmlplusplus/libxmlplusplus/blob/5.6.1/libxml%2B%2B/parsers/domparser.h>)
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
python3 parsarium.py build xml cpp libxmlpp
python3 parsarium.py run xml cpp libxmlpp controls/xml/catalog-ns.xml
```
