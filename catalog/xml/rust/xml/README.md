# xml — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.4.0`
- **Upstream:** [source repository](<https://github.com/kornelski/xml-rs>) · [crates.io](<https://crates.io/crates/xml>)
- **License:** MIT
- **Parser family:** xml-rs EventReader implementation in xml 1.4.0; xml-rs 1.0.0 is a re-export shim that depends on xml and is not a separate family
- **Local input API:** `xml::reader::EventReader::new(&[u8]); EventReader::next() -> Result<XmlEvent>; StartElement yields namespace-resolved OwnedName, attributes, and namespace map`
- **Documentation:** [API reference](<https://docs.rs/xml/1.4.0/xml/reader/struct.EventReader.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/xml/verification.json)

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
python3 parsarium.py build xml rust xml
python3 parsarium.py run xml rust xml controls/xml/catalog-ns.xml
```
