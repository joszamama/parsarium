# xml5ever — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.40.0`
- **License:** MIT OR Apache-2.0
- **Parser family:** Servo xml5ever XML5 tokenizer and tree builder; shares markup5ever primitives and design lineage with html5ever, but has own XML5 parser modules; markup5ever_rcdom is only a tree sink
- **Local input API:** `xml5ever::driver::parse_document(RcDom, XmlParseOpts) -> XmlParser<RcDom>; TendrilSink::one(&str) -> RcDom; xml5ever::tokenizer::XmlTokenizer::feed(BufferQueue) -> token events`
- **Documentation:** [API reference](<https://docs.rs/xml5ever/0.40.0/xml5ever/driver/fn.parse_document.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/xml5ever/verification.json)

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
python3 parsarium.py build xml rust xml5ever
python3 parsarium.py run xml rust xml5ever controls/xml/catalog-ns.xml
```
