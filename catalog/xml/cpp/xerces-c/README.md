# xerces-c — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.3.0`
- **Upstream:** [source repository](<https://github.com/apache/xerces-c>) · [Debian](<https://tracker.debian.org/pkg/xerces-c>)
- **License:** Apache-2.0
- **Parser family:** Apache Xerces-C++ scanner (IGXMLScanner)
- **Local input API:** `xercesc::XercesDOMParser::parse(const InputSource&) with xercesc::MemBufInputSource(const XMLByte*, XMLSize_t, ...) and setDoNamespaces(true), validation off, external DTD loading off`
- **Documentation:** [API reference](<https://xerces.apache.org/xerces-c/apiDocs-3/classMemBufInputSource.html>)
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
python3 parsarium.py build xml cpp xerces_c
python3 parsarium.py run xml cpp xerces_c controls/xml/catalog-ns.xml
```
