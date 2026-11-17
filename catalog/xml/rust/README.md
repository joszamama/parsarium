# XML / Rust — pilot

**Status:** pilot_four_paths_verified_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Four verified XML parser implementations selected within the first 100 hits of seven crates.io queries (642 hits, 483 unique), captured 2026-11-17. Twelve documented leads remain unverified. The xml-rs 1.0.0 package has 32,180,109 recent downloads but is a compatibility re-export of the xml package, so it is excluded as a duplicate family. Downloads include transitive pulls and are adoption proxies; ranks compare selected independent paths only. The xmlparser tokenizer does not resolve namespaces or validate tree structure; its adapter provides those observations. Two small UTF-8 controls without DOCTYPE do not establish DTD, external entity, non-UTF-8 encoding, XML 1.1, or redundant namespace redeclaration behavior. RustyXML 0.3.0 passed valid-control parsing but exact repeatable AFL++ feedback was not established; see data/rust/xml/rustyxml-feedback-audit.md.

[Ranking and search limits](../../../data/rust/xml/ranking.md) · [Standard API inventory](../../../data/rust/xml/standard.json)

## Third-party parsers

- [quick-xml](quick-xml/README.md) — verified Docker harness
- [roxmltree](roxmltree/README.md) — verified Docker harness
- [xml](xml/README.md) — verified Docker harness
- [xmlparser](xmlparser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
