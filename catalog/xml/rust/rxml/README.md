# rxml — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.14.0`
- **Upstream:** [source repository](<https://codeberg.org/jssfr/rxml>) · [crates.io](<https://crates.io/crates/rxml>)
- **License:** MIT
- **Parser family:** rxml (Jonas Schäfer) own lexer, raw parser and namespace resolver, with the same-author rxml_validation crate for name and character classes; minidom 0.19 is built on rxml and is not a separate family
- **Local input API:** `rxml::Parser::new() + rxml::Parse::parse_all(&mut &[u8], at_eof = true, FnMut(Event)) -> namespace-resolved events; rxml::RawParser::new() + parse_all -> raw attribute events`
- **Documentation:** [API reference](<https://docs.rs/rxml/0.14.0/rxml/struct.Parser.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/rxml/verification.json)

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
python3 parsarium.py build xml rust rxml
python3 parsarium.py run xml rust rxml controls/xml/catalog-ns.xml
```
