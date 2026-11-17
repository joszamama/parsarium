# rxml — XML / Rust

**Verified restricted XML 1.0 path in a bounded Rust XML pilot.** Release 0.14.0 parsed the shared namespace catalog control and a restricted copy of the shared order control. By design it has no DTD, custom entities or processing instructions, and it rejects comments by default.

- **Source:** [rxml 0.14.0 crate](https://static.crates.io/crates/rxml/rxml-0.14.0.crate), SHA-256 `4959705975475401c48b375deedd848d15b816c3915978fc617b31a1776fb60a`; repository [codeberg.org/jssfr/rxml](https://codeberg.org/jssfr/rxml).
- **License:** MIT; the release `COPYING` file and the same-author `rxml_validation` 0.12.0 dependency are pinned in [source-lock.json](../../../../projects/xml/rust/rxml/source-lock.json).
- **Local input API:** [`Parser::new`](https://docs.rs/rxml/0.14.0/rxml/struct.Parser.html) with [`Parse::parse_all`](https://docs.rs/rxml/0.14.0/rxml/trait.Parse.html#method.parse_all) over a local byte slice yields namespace-resolved events. A second pass through rxml's own `RawParser` counts `xmlns` declarations, which the resolver omits from `AttrMap`. Default options; crate built with `default-features = false, features = ["std"]`.
- **Parser family:** rxml's own lexer, raw parser and namespace resolver, with `rxml_validation` for name and character classes. minidom 0.19 builds on rxml and would share this family.
- **Adoption:** 961,809 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/xml/registry-snapshot.json), compared only with Rust XML paths. Downloads can include transitive pulls.
- **Controls:** [namespace catalog](../../../../controls/xml/catalog-ns.xml) and [restricted default namespace order](../../../../controls/xml/order-default-ns-restricted.xml).
- **Evidence:** [catalog record](../../../../data/rust/xml/parsers.json), [base receipt](../../../../projects/xml/rust/rxml/verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/xml/rust/rxml/verification.json).

## Observed result

The catalog control yielded a `{urn:parsarium:catalog}catalog` root, five expanded element names, two namespace declarations, decoded attributes, and text including `Café & té`. This equals the expat summary from `controls/xml/check_controls.py`.

The shared [order control](../../../../controls/xml/order-default-ns.xml) has a prolog comment and a processing instruction. rxml rejects it with `Error(RestrictedXml("comments"))`. The restricted copy removes only those two lines. expat gives the same summary for both files, and rxml matches it exactly: seven elements, three declarations, a default namespace reset, and decoded character references. Both exact summaries are pinned in the [manifest](../../../../projects/xml/rust/rxml/manifest.json).

The pinned crate documents these restrictions: no external resources, no DTD, no custom entities (only `lt`, `amp`, `gt`, `quot`, `apos`), no processing instructions, comments rejected unless `CommentMode::Discard` is set, UTF-8 only, `standalone` must be `yes` or absent, and XML 1.0 only. Names and attribute values are limited to 8,192 bytes by default. A local pre-check of `CommentMode::Discard` still rejected the no-PI order control, at the whitespace after its prolog comment, so the harness keeps rxml's default options. `AttrMap` lists attributes by namespace URI and local name, which matches document order on both controls. These controls establish only the observed behavior for these valid documents.

## Run

```sh
python3 parsarium.py build xml rust rxml
python3 parsarium.py run xml rust rxml controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml rust rxml
python3 parsarium.py afl prepare xml rust rxml runs/xml-rxml-afl
```

`afl prepare` seeds a run without starting a campaign. Verification checks both valid controls, rxml source coverage, and exact repeated input-dependent AFL++ feedback.
