# quick-xml — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.42.0`
- **License:** MIT
- **Parser family:** quick-xml pull reader (tafia/quick-xml)
- **Local input API:** `quick_xml::NsReader::from_reader(&[u8]); NsReader::read_event(); NsReader::resolver().resolve_element(..)/resolve_attribute(..); Attribute::normalized_value(XmlVersion::Implicit1_0); BytesText/BytesCData::xml10_content(); BytesRef::resolve_char_ref() with escape::resolve_predefined_entity`
- **Documentation:** [API reference](<https://docs.rs/quick-xml/0.42.0/quick_xml/reader/struct.NsReader.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../data/rust/xml/verification.json)

## Observed control result

```json
{
  "root": "{urn:parsarium:catalog}catalog",
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
  "attributes": [
    "version=1",
    "id=a1",
    "{urn:parsarium:catalog}lang=es",
    "id=b2"
  ],
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml rust quick_xml
python3 parsarium.py run xml rust quick_xml controls/xml/catalog-ns.xml
```
