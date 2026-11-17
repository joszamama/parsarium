# roxmltree — XML / Rust

**Verified path in a bounded pilot cell.** This release was run on two small valid XML 1.0 controls; the cell search remains open.

- **Pinned release:** `0.21.2`; [source crate](https://static.crates.io/crates/roxmltree/roxmltree-0.21.2.crate), SHA-256 `9da7f59328b09405b181fee1018925fad50f157afb43c0c0f5c522c256dd5907`.
- **License:** MIT OR Apache-2.0; both license files are hashed in [source-lock.json](../../../../projects/xml/rust/roxmltree/source-lock.json).
- **Parser family:** roxmltree 0.21.2 internal tokenizer and namespace-resolving tree builder. The pinned crate contains `src/tokenizer.rs` and depends on `memchr`, not on the separate `xmlparser` crate. Its historical relationship to xmlparser is recorded in the [lead](../../../../data/rust/xml/leads.json).
- **Local input API:** [`roxmltree::Document::parse(&str)`](https://docs.rs/roxmltree/0.21.2/roxmltree/struct.Document.html#method.parse), supplied with UTF-8 text decoded from a local file or byte buffer.
- **Adoption proxy:** 42,073,295 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/xml/registry-snapshot.json), ranked only against other verified Rust XML paths.
- **Valid controls:** [`catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml) and [`order-default-ns.xml`](../../../../controls/xml/order-default-ns.xml).
- **Evidence:** [catalog record](../../../../data/rust/xml/parsers.json), [base receipt](../../../../projects/xml/rust/roxmltree/verification.json), [AFL++ overlay](../../../../fuzzing/afl-native/xml/rust/roxmltree/verification.json).

## Observed structure

The adapter reports namespace-expanded element and attribute names, namespace declarations and URIs, nesting depth, and decoded text. On the first control:

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

The second control adds an empty default namespace and character references. Its exact expected result is pinned in the [manifest](../../../../projects/xml/rust/roxmltree/manifest.json). The adapter derives namespace declaration counts by comparing the parsed namespace scopes of each element and its parent; these controls contain no redundant redeclaration.

## Run this target

```sh
python3 parsarium.py build xml rust roxmltree
python3 parsarium.py run xml rust roxmltree controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml rust roxmltree
python3 parsarium.py afl prepare xml rust roxmltree runs/xml-roxmltree-afl
```

`afl prepare` seeds a run without starting a mutation campaign. The verification gate checks only the two valid controls, repeated AFL++ feedback, and roxmltree source coverage.
