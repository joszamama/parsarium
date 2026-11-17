# XML / Rust — pilot

**Status:** pilot_six_paths_verified_search_bounded; incomplete. 6 verified third-party paths, 0 verified standard APIs, 6 verified Docker harnesses.

Six verified XML parser implementations selected within the first 100 hits of seven crates.io queries (642 hits, 483 unique), captured 2026-11-17. Ten documented leads remain unverified. xml5ever 0.40.0 is an XML5 error-recovering superset parser: the two valid XML 1.0 controls verify namespace-aware output, but it does not establish strict XML 1.0 well-formedness, complete namespace behavior, DTD support, or other encodings. rxml 0.14.0 is a deliberately restricted XML 1.0 parser without DTDs, custom entities or processing instructions, and it rejects comments by default. It parses the shared catalog control exactly but rejects the shared order control (Error(RestrictedXml("comments"))), so its second control is order-default-ns-restricted.xml without that comment and processing instruction. The xml-rs 1.0.0 package is a compatibility re-export of xml and excluded as a duplicate family. Downloads include transitive pulls and are adoption proxies; ranks compare selected independent paths only. RustyXML 0.3.0 passed valid-control parsing but exact repeatable AFL++ feedback was not established; see data/rust/xml/rustyxml-feedback-audit.md.

[Ranking and search limits](../../../data/rust/xml/ranking.md) · [Standard API inventory](../../../data/rust/xml/standard.json)

## Third-party parsers

- [quick-xml](quick-xml/README.md) — verified Docker harness
- [roxmltree](roxmltree/README.md) — verified Docker harness
- [xml](xml/README.md) — verified Docker harness
- [xmlparser](xmlparser/README.md) — verified Docker harness
- [xml5ever](xml5ever/README.md) — verified Docker harness
- [rxml](rxml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
