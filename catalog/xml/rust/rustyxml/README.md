# RustyXML — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.3.0`
- **License:** MIT OR Apache-2.0
- **Parser family:** RustyXML (crate lib name xml; unrelated to the selected xml/xml-rs crate) own state-machine parser derived from ObjFW OFXMLParser per src/parser.rs; no runtime dependencies
- **Local input API:** `xml::Parser::new() + Parser::feed_str(&str), then Iterator<Item = Result<xml::Event, ParserError>>; Event::ElementStart(StartTag { name, ns, prefix, attributes: HashMap<(String, Option<String>), String> }), ElementEnd, Characters, CDATA, Comment, PI`
- **Documentation:** [API reference](<https://docs.rs/RustyXML/0.3.0/xml/struct.Parser.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/rustyxml/verification.json)

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
python3 parsarium.py build xml rust rustyxml
python3 parsarium.py run xml rust rustyxml controls/xml/catalog-ns.xml
```
