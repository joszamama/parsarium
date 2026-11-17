# XML / C++ — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: Xerces-C++ 3.3.0 and pugixml 1.16 were built and control-verified. Homebrew install-on-request (365d) orders the four differently: tinyxml2 1,757, pugixml 1,270, Xerces-C++ 1,209, libxml++ 461, so the order depends on the metric; Debian dev installs remain the one primary metric. Source-level popcon is not used because libxml++2.6's 79,794 count is a runtime pulled in by dependents (79,361 with no recent file access). tinyxml2 and libxml++ stay unresolved leads in leads.json. libxml++ parses through the libxml2 C library. Whole frameworks (Qt, Boost, POCO) were not ranked. The ISO C++ standard library has no XML API. pugixml does no namespace processing: its namespace-resolved output comes from adapter code over pugixml's qualified names, so namespace well-formedness is checked by the adapter, not the library. pugixml also skips DOCTYPE without expanding DTD entities. Two small UTF-8 controls without DOCTYPE do not establish DTD, entity declaration, validation, non-UTF-8 encoding or XML 1.1 behaviour; attributes are reported sorted per element because DOM NamedNodeMap order is unspecified.

[Ranking and search limits](../../../data/cpp/xml/ranking.md) · [Standard API inventory](../../../data/cpp/xml/standard.json)

## Third-party parsers

- [xerces-c](xerces-c/README.md) — verified Docker harness
- [pugixml](pugixml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
