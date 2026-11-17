# XML / C++ — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Three C++ XML paths are verified on a namespace-aware valid control, with source coverage and AFL feedback. TinyXML2 also passed a second valid control that omits a processing instruction; TinyXML2 11.0.0 rejects the same processing instruction in the shared order control. Both TinyXML2 and pugixml preserve qualified names but leave namespace resolution to the adapters, which is explicitly separated from library parsing. libxml++ remains unresolved and shares the libxml2 C parser family. The bounded search compared four named format-specific libraries using Debian -dev installs; Homebrew install-on-request gives a different order. Whole frameworks are not ranked by framework-wide installs. Two small valid UTF-8 controls cannot establish complete XML 1.0, DTD/entity, encoding or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/xml/ranking.md) · [Standard API inventory](../../../data/cpp/xml/standard.json)

## Third-party parsers

- [xerces-c](xerces-c/README.md) — verified Docker harness
- [pugixml](pugixml/README.md) — verified Docker harness
- [tinyxml2](tinyxml2/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
