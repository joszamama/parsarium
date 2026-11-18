# libcutl — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.10.0+ds1`
- **Upstream:** [Debian](<https://tracker.debian.org/pkg/libcutl>)
- **License:** MIT
- **Parser family:** Expat family: libcutl's own pull-event layer (cutl/xml/parser.cxx) over Expat
- **Local input API:** `cutl::xml::parser(std::istream&, input_name, receive_elements | receive_characters | receive_attributes_event | receive_namespace_decls) over a std::istringstream of the local bytes; next() until eof; qname().namespace_()/name() for start_element and start_attribute, value() for characters (inside start_attribute/end_attribute: the attribute value), start_namespace_decl events for xmlns declarations`
- **Documentation:** [API reference](<https://codesynthesis.com/projects/libcutl/>)
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
python3 parsarium.py build xml cpp libcutl
python3 parsarium.py run xml cpp libcutl controls/xml/catalog-ns.xml
```
