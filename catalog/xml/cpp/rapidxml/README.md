# rapidxml — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.13`
- **License:** BSL-1.0 OR MIT
- **Parser family:** RapidXML own in-situ DOM parser (rapidxml.hpp)
- **Local input API:** `rapidxml::xml_document<>::parse<0>(char*) on a mutable, zero-terminated local byte buffer; RapidXML parses in situ (it modifies the buffer) and does no namespace processing, so the adapter copies the input, appends the terminator and resolves prefixes from in-scope xmlns attributes`
- **Documentation:** [API reference](<https://rapidxml.sourceforge.net/manual.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/cpp/xml/parsers.json) · [control result](../../../../data/cpp/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "version=1",
    "id=a1",
    "{urn:parsarium:catalog}lang=es",
    "id=b2"
  ],
  "elements": [
    "{urn:parsarium:catalog}catalog",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}name",
    "{urn:parsarium:item}note"
  ],
  "max_depth": 3,
  "namespace_declarations": 2,
  "namespaces": [
    "urn:parsarium:catalog",
    "urn:parsarium:item"
  ],
  "root": "{urn:parsarium:catalog}catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Verification scope

RapidXML parses in situ: xml_document<>::parse<0>(char*) writes into the caller's mutable, zero-terminated buffer, so the adapter parses a copy. RapidXML keeps qualified names; namespace resolution is adapter code. Both shared valid controls pass; the default flags skip the order control's processing instruction instead of exposing it as a node. The control run covers 413 rapidxml.hpp lines; the parser-only AFL++ probe gives 38 and 45 repeat-stable tuples on the two controls (difference 15). Adoption is weak: Debian librapidxml-dev has 17 installations, none with recent use, and vendored or Boost.PropertyTree-embedded copies are not counted. Boost.PropertyTree's reader is RapidXML-derived, not a separate engine.

## Run this target

```sh
python3 parsarium.py build xml cpp rapidxml
python3 parsarium.py run xml cpp rapidxml controls/xml/catalog-ns.xml
```
