# quick-xml — XML / Rust

| | |
| --- | --- |
| Release | `0.42.0`, crates.io SHA-256 `41b1177fdf999d2321d3fb46ff47159d9c1fb9ad66a4879f8c50a0b504615e9b` |
| License | MIT |
| Source | [tafia/quick-xml](https://github.com/tafia/quick-xml/tree/v0.42.0) |
| Documentation | [docs.rs](https://docs.rs/quick-xml/0.42.0/quick_xml/reader/struct.NsReader.html) |
| Input API | `NsReader::from_reader(&[u8])`, `read_event()`, `resolver().resolve_element(..)` / `resolve_attribute(..)`, `Attribute::normalized_value(..)`, `BytesText::xml10_content()`, `BytesRef::resolve_char_ref()` |
| Family | quick-xml pull reader |
| Adoption | 178,628,779 crates.io recent downloads (90 days), 2026-11-17 |

## Control result

The harness passes the bytes of `controls/xml/catalog-ns.xml` to the namespace-aware reader from memory, with no temporary file, and reads every event to EOF.

```json
{"root": "{urn:parsarium:catalog}catalog",
 "elements": ["{urn:parsarium:catalog}catalog", "{urn:parsarium:item}item", "{urn:parsarium:item}item", "{urn:parsarium:item}name", "{urn:parsarium:item}note"],
 "max_depth": 3, "namespace_declarations": 2, "namespaces": ["urn:parsarium:catalog", "urn:parsarium:item"],
 "attributes": ["version=1", "id=a1", "{urn:parsarium:catalog}lang=es", "id=b2"],
 "text": ["Café & té", "Zürich <HQ>", "x < y"]}
```

The default namespace applies to the unprefixed `item` elements but not to the unprefixed attributes. The text entries come from `&amp;`, `&lt;` and `&gt;` references and a CDATA section. `controls/xml/check_controls.py` builds the same summary with expat.

The fixed second control, `order-default-ns.xml`, gives seven elements with a depth of four. The last two, `plain` and `leaf`, are in no namespace after `xmlns=""`. Its attributes are `n=1`, `{urn:parsarium:price}currency=EUR`, `n=2` and `note=say "hi"`, and its text is `A-7` and `12.50 €` from character references.

## Limits

The harness resolves only the five predefined entities. A document with a DOCTYPE is read, but its declarations are not applied. The controls have no DOCTYPE, external entities, non-UTF-8 encoding, XML 1.1 declaration, or attribute whitespace to normalize, so none of those cases is tested. quick-xml is not a validating parser, and this harness checks only end-tag names, not every XML 1.0 well-formedness constraint.

The afl.rs build instruments the whole fuzz binary, including memchr, serde_json, and the harness, so the edge counts are not parser-only. The AFL++ receipt shows that the two controls produce different parser behavior. Each control gives the same edges on all three repeats (1,152 and 1,344). Each control also has edges the other lacks (66 and 258). Seven quick-xml source files are covered differently; `escape.rs` rises from 49 to 153 lines with the character references in the second control.
