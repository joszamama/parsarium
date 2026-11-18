# xmlparser — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.13.6`
- **Upstream:** [source repository](<https://github.com/RazrFalcon/xmlparser>) · [crates.io](<https://crates.io/crates/xmlparser>)
- **License:** MIT OR Apache-2.0
- **Parser family:** xmlparser 0.13.6 own low-level XML tokenizer; distinct pinned source from roxmltree 0.21.2 internal tokenizer, with documented historical relationship
- **Local input API:** `xmlparser::Tokenizer::from(&str) -> Iterator<Item=Result<Token, Error>>; Token::{ElementStart, Attribute, ElementEnd, Text, Cdata}`
- **Documentation:** [API reference](<https://docs.rs/xmlparser/0.13.6/xmlparser/struct.Tokenizer.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/xmlparser/verification.json)

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
python3 parsarium.py build xml rust xmlparser
python3 parsarium.py run xml rust xmlparser controls/xml/catalog-ns.xml
```
