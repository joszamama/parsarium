# uppsala — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.12.1`
- **Upstream:** [source repository](<https://github.com/kushaldas/uppsala>) · [crates.io](<https://crates.io/crates/uppsala>)
- **License:** BSD-2-Clause
- **Parser family:** uppsala pure-Rust XML scanner, recursive-descent parser, namespace resolver, and DOM; no external parser dependency
- **Local input API:** `uppsala::parse_bytes(&[u8]) -> XmlResult<Document>; DOM NodeKind::Element/Text/CData and QName.namespace_uri/local_name, element.attributes and namespace_declarations`
- **Documentation:** [API reference](<https://docs.rs/uppsala/0.12.1/uppsala/fn.parse_bytes.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/uppsala/verification.json)

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
python3 parsarium.py build xml rust uppsala
python3 parsarium.py run xml rust uppsala controls/xml/catalog-ns.xml
```
