# xml5ever — XML / Rust

**Verified XML5 path in a bounded Rust XML pilot.** Release 0.40.0 parsed two small valid XML 1.0 controls. Its XML5 recovery grammar is broader than strict XML 1.0 well-formedness.

- **Source:** [xml5ever 0.40.0 crate](https://static.crates.io/crates/xml5ever/xml5ever-0.40.0.crate), SHA-256 `73290529dc9bc6c6155bf77fdd70ce0061f98ad387586aa3104cddab29206961`.
- **License:** MIT OR Apache-2.0; release license files and the separate tree-sink package are pinned in [source-lock.json](../../../../projects/xml/rust/xml5ever/source-lock.json).
- **Local input API:** [`driver::parse_document`](https://docs.rs/xml5ever/0.40.0/xml5ever/driver/fn.parse_document.html) receives local UTF-8 text through `TendrilSink::one` and builds a DOM with `markup5ever_rcdom::RcDom`; `XmlTokenizer::feed` provides token events in a separate pass.
- **Parser family:** Servo xml5ever XML5 tokenizer and tree builder. It shares markup5ever primitives and html5ever design lineage. `markup5ever_rcdom` only stores the resulting tree.
- **Adoption:** 14,338,073 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/xml/registry-snapshot.json), compared only with Rust XML paths. Downloads can include transitive pulls.
- **Controls:** [namespace catalog](../../../../controls/xml/catalog-ns.xml) and [default namespace order](../../../../controls/xml/order-default-ns.xml).
- **Evidence:** [catalog record](../../../../data/rust/xml/parsers.json), [base receipt](../../../../projects/xml/rust/xml5ever/verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/xml/rust/xml5ever/verification.json).

## Observed result

The catalog control yielded a `{urn:parsarium:catalog}catalog` root, five expanded element names, two namespace declarations, decoded attributes, and text including `Café & té`. The order control yielded seven elements, three declarations, a default namespace reset, and decoded character references. Both exact summaries are pinned in the [manifest](../../../../projects/xml/rust/xml5ever/manifest.json).

The tree builder resolves element and attribute names and drops namespace declarations from DOM attributes. The harness counts declarations from a second pass through xml5ever's tokenizer. The release README says XML5 favors error recovery, offers partial namespace support, and does not parse DTDs. These controls establish only the observed behavior for these valid documents.

## Run

```sh
python3 parsarium.py build xml rust xml5ever
python3 parsarium.py run xml rust xml5ever controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml rust xml5ever
python3 parsarium.py afl prepare xml rust xml5ever runs/xml-xml5ever-afl
```

`afl prepare` seeds a run without starting a campaign. Verification checks both valid controls, xml5ever source coverage, and exact repeated input-dependent AFL++ feedback.
