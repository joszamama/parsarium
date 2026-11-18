# tinyxml2 — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `11.0.0`
- **Upstream:** [source repository](<https://github.com/leethomason/tinyxml2>) · [Debian](<https://tracker.debian.org/pkg/tinyxml2>)
- **License:** Zlib
- **Parser family:** TinyXML2 own in-memory XML parser
- **Local input API:** `tinyxml2::XMLDocument::Parse(const char* xml, size_t nBytes) over a local byte buffer; TinyXML2 does no namespace processing, so the adapter resolves prefixes from in-scope xmlns attributes`
- **Documentation:** [API reference](<https://leethomason.github.io/tinyxml2/classtinyxml2_1_1_x_m_l_document.html>)
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
python3 parsarium.py build xml cpp tinyxml2
python3 parsarium.py run xml cpp tinyxml2 controls/xml/catalog-ns.xml
```
