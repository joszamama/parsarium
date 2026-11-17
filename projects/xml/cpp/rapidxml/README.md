# RapidXML 1.13 — C++ / XML candidate

RapidXML's documented `xml_document<>::parse<0>(char*)` parses a local, mutable, zero terminated XML buffer into its own DOM. The harness copies input bytes, appends the terminator, parses, then reports the observed element tree, attributes, namespaces, and text. RapidXML preserves qualified names; namespace resolution in the result is adapter code. It does not claim validation or complete XML conformance.

The pinned source archive is Debian's unmodified upstream RapidXML 1.13 tarball. `rapidxml.hpp` is the parser family; Boost.PropertyTree includes a RapidXML-derived reader and should not be counted as an independent parser engine.

Both valid controls pass with their exact expected structures. The Docker source coverage is for `rapidxml.hpp`, separately from the adapter. `parser-probe.cpp` invokes only `xml_document::parse<0>` and a root existence check. The AFL++ build allowlists the RapidXML header, so adapter namespace traversal and JSON reporting do not contribute feedback. The [differential receipt](../../../../fuzzing/afl-native/xml/cpp/rapidxml/differential.json) records three repeat-stable maps on each control.

From the repository root:

```sh
python3 parsarium.py build xml cpp rapidxml
python3 parsarium.py run xml cpp rapidxml controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml cpp rapidxml
python3 parsarium.py afl prepare xml cpp rapidxml runs/xml-rapidxml-afl
```

Debian popcon `librapidxml-dev` records 17 installed packages in the saved snapshot, with zero recent-use votes. This is a comparable `-dev` package count to the other ranked C++ XML libraries, but a weak adoption signal. The candidate is deliberately separate from the selected catalog and ranking pending curation.
