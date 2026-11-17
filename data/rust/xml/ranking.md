# RUST × XML: selected parsers

8 control-verified third-party paths; bounded pilot scope. The ceiling is ten and the cell is not padded. XML parser leads that have not yet been run are listed in [leads.json](leads.json).

## Primary within-cell adoption metric

crates.io recent downloads (90 days), from the search API in [registry-snapshot.json](registry-snapshot.json), captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [quick-xml](https://docs.rs/quick-xml/0.42.0/quick_xml/) | 0.42.0 | 178,628,779 | Namespace-resolved event stream: element and attribute expanded names, namespace declarations, decoded text and CDATA | quick-xml pull reader |
| 2 | [xmlparser](https://docs.rs/xmlparser/0.13.6/xmlparser/struct.Tokenizer.html) | 0.13.6 | 52,247,004 | `Tokenizer::from` over local UTF-8 text; adapter resolves namespace names, references and depth | xmlparser low-level tokenizer |
| 3 | [roxmltree](https://docs.rs/roxmltree/0.21.2/roxmltree/struct.Document.html#method.parse) | 0.21.2 | 42,073,295 | Namespace-resolved DOM: expanded names, attributes, namespace declarations, decoded text | roxmltree internal tokenizer and tree builder |
| 4 | [xml5ever](https://docs.rs/xml5ever/0.40.0/xml5ever/) | 0.40.0 | 14,338,073 | XML5 recovery parser builds namespace-resolved DOM from local UTF-8 input; own tokenizer pass counts declarations | Servo xml5ever tokenizer and tree builder |
| 5 | [xml](https://docs.rs/xml/1.4.0/xml/reader/struct.EventReader.html) | 1.4.0 | 6,413,267 | `EventReader` over local bytes: namespace-expanded elements and attributes, declarations, decoded text | xml-rs EventReader implementation |
| 6 | [RustyXML](https://docs.rs/RustyXML/0.3.0/xml/struct.Parser.html) | 0.3.0 | 4,342,774 | `Parser::new()` + `feed_str(&str)` over locally decoded UTF-8 text: namespace-resolved SAX-like events, xmlns attributes counted as declarations, decoded text and CDATA | RustyXML own state-machine parser derived from ObjFW OFXMLParser |
| 7 | [rxml](https://docs.rs/rxml/0.14.0/rxml/struct.Parser.html) | 0.14.0 | 961,809 | Restricted XML 1.0 `Parser` over local bytes: namespace-resolved events; own `RawParser` pass counts declarations | rxml lexer, raw parser and namespace resolver |
| 8 | [uppsala](https://docs.rs/uppsala/0.12.1/uppsala/fn.parse_bytes.html) | 0.12.1 | 287,733 | `parse_bytes(&[u8])` over local bytes: namespace-aware DOM with expanded element and attribute names, declarations, decoded text | uppsala own scanner, recursive-descent parser, namespace resolver and DOM |

Unverified XML parser leads, by the same metric: xml-no-std 1,648,161 (shared family), minidom 984,597 (shared rxml family), instant-xml 748,214, sxd-document 647,390, libxml 621,059, minidom-14 391,747 (shared family), hard-xml 228,546 (shared family), xot 112,374 (shared family). Recent downloads include transitive dependency pulls. windows (113,676,999) and pulldown-cmark (73,457,258) rank above several leads in the search results but are not XML parsers.

## Standard library

None documented in the Rust 1.99.1 standard library; see [standard.json](standard.json).

Ranks compare only verified paths. The xmlparser tokenizer does not resolve namespaces or validate nesting; its adapter supplies those observations on the two valid controls. The pinned roxmltree 0.21.2 crate has its own `src/tokenizer.rs` and no xmlparser dependency; its historical relationship to xmlparser is retained in [leads.json](leads.json).

The `xml-rs` 1.0.0 package is excluded as a duplicate: its release contains a re-export of the `xml` crate, which owns the EventReader parser. Its 32,180,109 recent downloads are recorded in [leads.json](leads.json) but do not become an independent parser rank.

RustyXML 0.3.0 (MIT OR Apache-2.0, crate SHA-256 pinned; library name `xml`, unrelated to the selected `xml` crate) documents `Parser::new()` and `feed_str(&str)`; the adapter decodes local bytes as UTF-8 and iterates the parser's events. Its `src/parser.rs` states that the parser derives from ObjFW's OFXMLParser; the crate has no runtime dependencies. RustyXML resolves element and attribute prefixes itself and keeps `xmlns` attributes in `StartTag.attributes`, a HashMap, so the adapter sorts each element's attributes by (namespace, local name), which matches document order on both controls. Both shared valid controls match the Expat oracle exactly. Docker covers 285 RustyXML lines (266 in `src/parser.rs` on the catalog control, 281 on the order control). The README lists incomplete error checking, so the valid controls do not establish strict XML 1.0 well-formedness checking. AFL++ instrumentation is restricted to the RustyXML crate. Its own HashMaps take per-process SipHash keys from `getrandom`, which changed a few probe-path edges between identical runs; the overlay preloads a shim that returns constant `getrandom` bytes, without changing parser code or output. With that setting, ten `afl-showmap` maps per control are identical (668 and 733 edges, 59 and 124 unique to each control); see [feedback audit](rustyxml-feedback-audit.md).

xml5ever 0.40.0 uses an XML5 recovery grammar. The two valid XML 1.0 controls give exact namespace-aware structure, but this path is not a strict XML 1.0 well-formedness validator. Its pinned README says namespace support is partial and DTD parsing is outside its scope. The separate markup5ever_rcdom dependency is only the tree sink; xml5ever owns the tokenizer and tree builder.

rxml 0.14.0 parses a restricted XML 1.0 subset by design: no DTD, custom entities or processing instructions, UTF-8 only, and comments rejected unless `CommentMode::Discard` is set. It parses the shared catalog control exactly. With default options it rejects the shared order control with `RestrictedXml("comments")`; that control also contains a processing instruction. Its second control, `order-default-ns-restricted.xml`, removes only those two lines and has the same expat summary. AttrMap lists attributes by namespace URI and local name, which matches document order on both controls.

uppsala 0.12.1 (BSD-2-Clause, crate SHA-256 pinned) documents `parse_bytes(&[u8])`, which detects UTF-8/UTF-16 and runs the crate's own `Parser` into a namespace-aware DOM. The pinned crate has no runtime dependencies; its scanner, recursive-descent parser (`src/parser.rs`, `src/pull.rs`) and namespace resolver do not wrap quick-xml, xmlparser, roxmltree or xml. Both shared valid controls match the Expat oracle exactly. Docker covers 909 uppsala source lines (234 in `src/parser.rs` on the catalog control, 304 on the order control). AFL++ instrumentation is restricted to the uppsala crate; repeated `afl-showmap` maps are identical (1,114 and 1,285 edges, 94 and 265 unique to each control). The crate also ships XPath, XSD and XSLT modules that these controls do not exercise.
