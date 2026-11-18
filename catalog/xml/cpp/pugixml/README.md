# pugixml — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.16`
- **Upstream:** [source repository](<https://github.com/zeux/pugixml>) · [Debian](<https://tracker.debian.org/pkg/pugixml>)
- **License:** MIT
- **Parser family:** pugixml own recursive-descent parser (pugi::impl::xml_parser)
- **Local input API:** `pugi::xml_document::load_buffer(const void*, size_t, parse_default, encoding_utf8); pugixml does no namespace processing, so the adapter resolves prefixes from in-scope xmlns attributes and rejects unbound prefixes and duplicate expanded attributes`
- **Documentation:** [API reference](<https://pugixml.org/docs/manual.html#loading.memory>)
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
python3 parsarium.py build xml cpp pugixml
python3 parsarium.py run xml cpp pugixml controls/xml/catalog-ns.xml
```
