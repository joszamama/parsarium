# xml — XML / Rust

**Verified path in a bounded pilot cell.** This release was run on two small valid XML 1.0 controls; the cell search remains open.

- **Pinned release:** `xml` `1.4.0`; [source crate](https://static.crates.io/crates/xml/xml-1.4.0.crate), SHA-256 `2f45bb2c13fec6a6cb4c0f76a7e94839e110a14ec803ec2940777a94c347bc52`.
- **License:** MIT; the release license file is hashed in [source-lock.json](../../../../projects/xml/rust/xml/source-lock.json).
- **Parser family:** the xml-rs project's EventReader implementation, published as crate `xml`. The separately published `xml-rs` 1.0.0 package is a compatibility re-export with only a dependency on `xml`; it is recorded as an excluded duplicate in [leads.json](../../../../data/rust/xml/leads.json).
- **Local input API:** [`xml::reader::EventReader::new(&[u8])`](https://docs.rs/xml/1.4.0/xml/reader/struct.EventReader.html) followed by `next()`, yielding namespace-resolved start/end events and decoded text.
- **Adoption proxy:** 6,413,267 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/xml/registry-snapshot.json), ranked only against verified independent Rust XML paths.
- **Valid controls:** [`catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml) and [`order-default-ns.xml`](../../../../controls/xml/order-default-ns.xml).
- **Evidence:** [catalog record](../../../../data/rust/xml/parsers.json), [base receipt](../../../../projects/xml/rust/xml/verification.json), [AFL++ overlay](../../../../fuzzing/afl-native/xml/rust/xml/verification.json).

## Observed structure

The adapter reports namespace-expanded element and attribute names, declarations and URIs, nesting depth, and decoded text. On the first control:

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

The second control adds an empty default namespace and character references. Its exact expected output is pinned in the [manifest](../../../../projects/xml/rust/xml/manifest.json). Namespace declarations are counted by comparing the parsed namespace maps of each element and its parent; these controls contain no redundant redeclaration.

## Run this target

```sh
python3 parsarium.py build xml rust xml
python3 parsarium.py run xml rust xml controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml rust xml
python3 parsarium.py afl prepare xml rust xml runs/xml-xml-afl
```

`afl prepare` seeds a run without starting a mutation campaign. The verification gate checks only the two valid controls, repeated AFL++ feedback, and xml EventReader parser source coverage.
