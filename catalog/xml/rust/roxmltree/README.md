# roxmltree — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.21.2`
- **Upstream:** [source repository](<https://github.com/RazrFalcon/roxmltree>) · [crates.io](<https://crates.io/crates/roxmltree>)
- **License:** MIT OR Apache-2.0
- **Parser family:** roxmltree 0.21.2 internal tokenizer and namespace-resolving tree builder; no xmlparser crate dependency in pinned source (historical xmlparser relationship recorded in lead)
- **Local input API:** `roxmltree::Document::parse(&str) -> Result<Document, Error>; Document::descendants(); Node::tag_name()/attributes()/namespaces()/text()`
- **Documentation:** [API reference](<https://docs.rs/roxmltree/0.21.2/roxmltree/struct.Document.html#method.parse>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/roxmltree/verification.json)

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
python3 parsarium.py build xml rust roxmltree
python3 parsarium.py run xml rust roxmltree controls/xml/catalog-ns.xml
```
