# XML / C++ — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

All five C++ XML paths pass the namespace-aware catalog control with source coverage and AFL++ feedback. Xerces-C++, pugixml, libxml++ and RapidXML pass the shared second valid control; TinyXML2 uses a no-processing-instruction variant because it rejects that instruction, while RapidXML's default flags skip it. libxml++ parser-only feedback and native libxml2 parser.c lines are repeatable and input-dependent. The bounded search covered five named format-specific libraries, so other C++ XML packages remain unmeasured. Homebrew install-on-request orders the first three differently and its libxml++ formula is an older ABI; RapidXML has no Homebrew formula. The libxml++ 275 Debian dev installs sum three ABIs, while its matching ABI-5 package has seven. RapidXML's 17 librapidxml-dev installations, none with recent use, are a weak adoption signal and exclude vendored or Boost-embedded copies. Two small valid UTF-8 controls cannot establish complete XML 1.0, DTD/entity, encoding or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/xml/ranking.md) · [Standard API inventory](../../../data/cpp/xml/standard.json)

## Third-party parsers

- [xerces-c](xerces-c/README.md) — verified Docker harness
- [pugixml](pugixml/README.md) — verified Docker harness
- [tinyxml2](tinyxml2/README.md) — verified Docker harness
- [libxml++](libxml/README.md) — verified Docker harness
- [rapidxml](rapidxml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
