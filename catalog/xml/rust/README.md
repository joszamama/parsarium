# XML / Rust — pilot

**Status:** pilot_nine_paths_verified_search_bounded; incomplete. 9 verified third-party paths, 0 verified standard APIs, 9 verified Docker harnesses.

Nine verified XML parser paths selected within the first 100 hits of seven crates.io queries (642 hits, 483 unique), captured 2026-11-17. Seven documented leads remain unverified. xml5ever 0.40.0 is an XML5 error-recovering superset parser: the two valid XML 1.0 controls verify namespace-aware output, but it does not establish strict XML 1.0 well-formedness, complete namespace behavior, DTD support, or other encodings. rxml 0.14.0 is a deliberately restricted XML 1.0 parser without DTDs, custom entities or processing instructions, and it rejects comments by default. It parses the shared catalog control exactly but rejects the shared order control (Error(RestrictedXml("comments"))), so its second control is order-default-ns-restricted.xml without that comment and processing instruction. The xml-rs 1.0.0 package is a compatibility re-export of xml and excluded as a duplicate family. minidom 0.19.0 is a DOM wrapper over the selected rxml family: rxml's RawReader lexes and parses, and minidom's own TreeBuilder resolves prefixes and builds the tree. It inherits rxml's restricted subset, so it also rejects the shared order control and uses the restricted order control; its stable AFL++ edge differential has no change in minidom source-line counts, and the differing lines are in rxml. uppsala 0.12.1 parses both shared valid controls through its own namespace-aware DOM parser; the controls do not establish its XPath, XSD or XSLT features, DTD handling, other encodings, or complete XML 1.0 conformance. Downloads include transitive pulls and are adoption proxies; ranks compare selected paths only, and the minidom and rxml counts overlap because minidom depends on rxml. RustyXML 0.3.0 parses both shared valid controls through its own ObjFW-derived streaming parser; its README lists incomplete error checking, so the controls do not establish strict XML 1.0 well-formedness checking, DTD handling or non-UTF-8 encodings. Its AFL++ overlay fixes std HashMap RandomState keys with a getrandom AFL_PRELOAD shim; see data/rust/xml/rustyxml-feedback-audit.md.

[Ranking and search limits](../../../data/rust/xml/ranking.md) · [Standard API inventory](../../../data/rust/xml/standard.json)

## Third-party parsers

- [quick-xml](quick-xml/README.md) — verified Docker harness
- [roxmltree](roxmltree/README.md) — verified Docker harness
- [xml](xml/README.md) — verified Docker harness
- [xmlparser](xmlparser/README.md) — verified Docker harness
- [xml5ever](xml5ever/README.md) — verified Docker harness
- [rxml](rxml/README.md) — verified Docker harness
- [uppsala](uppsala/README.md) — verified Docker harness
- [RustyXML](rustyxml/README.md) — verified Docker harness
- [minidom](minidom/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
