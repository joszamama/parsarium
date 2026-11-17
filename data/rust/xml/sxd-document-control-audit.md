# sxd-document 0.3.2 valid-control check

The pinned crate's documented `sxd_document::parser::parse(&str)` API parsed both local UTF-8 controls with Rust 1.99.1. The `sxd-document-0.3.2.crate` archive SHA-256 is `94d82f37be9faf1b10a82c4bd492b74f698e40082f0f40de38ab275f31d42078`. This is a lead check, not a selected or runnable Parsarium path.

For `controls/xml/catalog-ns.xml`, the DOM reported the root as `{urn:parsarium:catalog}catalog` but its descendants as `item`, `name`, and `note`, with no namespace URI. The expected expanded names use `{urn:parsarium:item}`. Its `namespaces_in_scope()` on the root included only the prefixed `c` namespace and the built-in `xml` namespace; the default `xmlns="urn:parsarium:item"` was absent. Entity text split across adjacent DOM text nodes but can be joined by an adapter.

The [pinned parser source](https://docs.rs/crate/sxd-document/0.3.2/source/src/parser.rs) in `finish_opening_tag` reads `default_namespace`, but only applies it in the unprefixed-element branch. For a prefixed root, it creates the element from the prefix mapping and skips registering the simultaneous default namespace. This explains the observed DOM result. Reconstructing the missing namespace from raw input in the adapter would require another XML parser, so the package remains unresolved for this cell's controls. No fuzzing or malformed inputs were used.
