# minidom — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.19.0`
- **Upstream:** [source repository](<https://gitlab.com/xmpp-rs/xmpp-rs>) · [crates.io](<https://crates.io/crates/minidom>)
- **License:** MPL-2.0
- **Parser family:** rxml (shared with the selected rxml path): rxml lexer and RawParser via RawReader; minidom adds its own TreeBuilder prefix resolution and DOM. Not an independent tokenizer.
- **Local input API:** `minidom::Element::from_reader(impl BufRead) -> Result<Element>; Element::name()/ns()/attrs() (rxml AttrMap keyed by namespace URI and local name), Element::prefixes.declared_prefixes(), Element::nodes() -> Node::Element/Node::Text`
- **Documentation:** [API reference](<https://docs.rs/minidom/0.19.0/minidom/element/struct.Element.html#method.from_reader>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/minidom/verification.json)

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
python3 parsarium.py build xml rust minidom
python3 parsarium.py run xml rust minidom controls/xml/catalog-ns.xml
```
