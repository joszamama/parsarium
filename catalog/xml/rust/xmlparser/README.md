# xmlparser — XML / Rust

**Verified path in a bounded pilot cell.** Pinned release 0.13.6 was run on two small, valid UTF-8 XML 1.0 controls. This is a low-level token parser, and the cell search remains open.

- **Source:** [xmlparser 0.13.6 crate](https://static.crates.io/crates/xmlparser/xmlparser-0.13.6.crate), SHA-256 `66fee0b777b0f5ac1c69bb06d361268faafa61cd4682ae064a171c16c433e9e4`.
- **License:** MIT OR Apache-2.0. Both release license file hashes are pinned in [source-lock.json](../../../../projects/xml/rust/xmlparser/source-lock.json).
- **Input API:** [`Tokenizer::from(&str)`](https://docs.rs/xmlparser/0.13.6/xmlparser/struct.Tokenizer.html) yields element, attribute, text and CDATA tokens from local UTF-8 text. The harness reads local bytes and converts them to UTF-8.
- **Parser family:** xmlparser's own zero-allocation tokenizer. The pinned roxmltree 0.21.2 has a separate internal tokenizer; the projects share historical authorship.
- **Adoption:** 52,247,004 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/xml/registry-snapshot.json), compared only with Rust XML paths. Downloads include transitive dependency pulls.
- **Controls:** [namespace catalog](../../../../controls/xml/catalog-ns.xml) and [default namespace order](../../../../controls/xml/order-default-ns.xml).
- **Evidence:** [catalog record](../../../../data/rust/xml/parsers.json), [base verification](../../../../projects/xml/rust/xmlparser/verification.json), [AFL++ verification](../../../../fuzzing/afl-native/xml/rust/xmlparser/verification.json).

## Observed result

The adapter resolves declared namespaces, validates matching element nesting, decodes predefined and numeric character references, and reports the root, ordered expanded element names and attributes, maximum depth, namespace declarations and URIs, and nonempty text. The first control yields a `{urn:parsarium:catalog}catalog` root, five elements, two namespace declarations, depth three, and decoded text including `Café & té`. Both exact expected summaries are pinned in the [manifest](../../../../projects/xml/rust/xmlparser/manifest.json).

The tokenizer itself does not resolve namespaces, validate nesting, or expand entity references. The adapter provides those observations for the two controls. DTDs, external entities, non-UTF-8 encodings, XML 1.1, and redundant namespace redeclarations remain untested.

## Run

```sh
python3 parsarium.py build xml rust xmlparser
python3 parsarium.py run xml rust xmlparser controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml rust xmlparser
python3 parsarium.py afl prepare xml rust xmlparser runs/xml-xmlparser-afl
```

`afl prepare` sets up a seeded run without starting a campaign. Verification uses only the two valid controls and requires covered xmlparser source and stable, input-dependent AFL++ feedback.
