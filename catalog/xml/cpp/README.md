# XML / C++ — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

All four C++ XML paths pass the namespace-aware catalog control with source coverage and AFL++ feedback. Xerces-C++, pugixml and libxml++ pass the shared second valid control; TinyXML2 uses a no-processing-instruction variant because it rejects that instruction. libxml++ parser-only feedback and native libxml2 parser.c lines are repeatable and input-dependent. The bounded search covered four named format-specific libraries, so other C++ XML packages remain unmeasured. Homebrew install-on-request orders the first three differently and its libxml++ formula is an older ABI. The libxml++ 275 Debian dev installs sum three ABIs, while its matching ABI-5 package has seven. Two small valid UTF-8 controls cannot establish complete XML 1.0, DTD/entity, encoding or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/xml/ranking.md) · [Standard API inventory](../../../data/cpp/xml/standard.json)

## Third-party parsers

- [xerces-c](xerces-c/README.md) — verified Docker harness
- [pugixml](pugixml/README.md) — verified Docker harness
- [tinyxml2](tinyxml2/README.md) — verified Docker harness
- [libxml++](libxml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
