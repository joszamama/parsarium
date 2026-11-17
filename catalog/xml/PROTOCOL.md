# XML cell protocol

This cell applies the [general protocol](../../PROTOCOL.md) to XML 1.0 documents encoded in UTF-8, with Namespaces in XML 1.0. SVG is a separate cell; an SVG renderer can pass there without reporting generic XML structure.

## Eligibility

A path qualifies only if it reads XML markup from local bytes, a local file, or a stream and reports what it parsed. Serializers, typed serde mappers without a generic element view, HTML tokenizers, grammar generators, and signature detectors are excluded or left as leads in `data/<ecosystem>/xml/leads.json`.

The observed result must come from the markup. The harness reports the root and every element as an expanded `{namespace}local` name in document order, the maximum depth, the count of namespace declarations and the distinct namespace URIs they bind, every non-declaration attribute as an expanded name and value, and the trimmed, non-empty runs of decoded character data between markup. Decoding covers predefined entity references, character references, and CDATA sections.

## Controls

- `controls/xml/catalog-ns.xml`: the primary control, 271 bytes. A prefixed root, a default namespace, an unprefixed and a prefixed attribute, `&amp;` `&lt;` `&gt;`, a CDATA section, and non-ASCII text.
- `controls/xml/order-default-ns.xml`: the fixed second control for AFL++ feedback, 334 bytes. A comment before the root, a processing instruction, single-quoted attributes, `&quot;` in an attribute, hexadecimal and decimal character references, an empty element, and an `xmlns=""` undeclaration.

Both files are well-formed, have an XML declaration, and contain no DOCTYPE, tabs, or carriage returns. `controls/xml/check_controls.py` parses them with expat through the Python standard library and builds the same summary; it is the independent oracle for the expected outputs. `xmllint --noout` also accepts both files.

## Adoption

Paths are ranked within one ecosystem by its registry metric. For Rust, this is the crates.io 90-day recent downloads returned by the recorded search snapshot. Crates built on a selected parser are recorded as shared-family leads. The ceiling is ten paths, and the cell is not padded.

## AFL++

The overlay must show parser-derived feedback on both controls. Each control runs three times under `afl-showmap`, and the receipt records the edge counts, stable edges, edges unique to each control, and per-file parser source lines. The overlay checks only launchers and feedback. It runs no campaign and tests no malformed inputs.
