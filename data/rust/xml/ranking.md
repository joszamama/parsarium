# RUST × XML: selected parsers

3 control-verified third-party paths; bounded pilot scope. The ceiling is ten and the cell is not padded. XML parser leads that have not yet been run are listed in [leads.json](leads.json).

## Primary within-cell adoption metric

crates.io recent downloads (90 days), from the search API in [registry-snapshot.json](registry-snapshot.json), captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [quick-xml](https://docs.rs/quick-xml/0.42.0/quick_xml/) | 0.42.0 | 178,628,779 | Namespace-resolved event stream: element and attribute expanded names, namespace declarations, decoded text and CDATA | quick-xml pull reader |
| 2 | [roxmltree](https://docs.rs/roxmltree/0.21.2/roxmltree/struct.Document.html#method.parse) | 0.21.2 | 42,073,295 | Namespace-resolved DOM: expanded names, attributes, namespace declarations, decoded text | roxmltree internal tokenizer and tree builder |
| 3 | [xml](https://docs.rs/xml/1.4.0/xml/reader/struct.EventReader.html) | 1.4.0 | 6,413,267 | `EventReader` over local bytes: namespace-expanded elements and attributes, declarations, decoded text | xml-rs EventReader implementation |

Unverified XML parser leads, by the same metric: xmlparser 52,247,004, xml5ever 14,338,073, RustyXML 4,342,774, xml-no-std 1,648,161 (shared family), minidom 984,597 (shared family), rxml 961,809, instant-xml 748,214, sxd-document 647,390, libxml 621,059, minidom-14 391,747 (shared family), uppsala 287,733, hard-xml 228,546 (shared family), xot 112,374 (shared family). Recent downloads include transitive dependency pulls. windows (113,676,999) and pulldown-cmark (73,457,258) rank above several leads in the search results but are not XML parsers.

## Standard library

None documented in the Rust 1.99.1 standard library; see [standard.json](standard.json).

Ranks compare only verified paths. The higher-download xmlparser remains unverified. The pinned roxmltree 0.21.2 crate has its own `src/tokenizer.rs` and no xmlparser dependency; its historical relationship to xmlparser is retained in [leads.json](leads.json).

The `xml-rs` 1.0.0 package is excluded as a duplicate: its release contains a re-export of the `xml` crate, which owns the EventReader parser. Its 32,180,109 recent downloads are recorded in [leads.json](leads.json) but do not become an independent parser rank.
