# C++ × XML: selected parsers

4 control-verified third-party paths selected from four searched format-specific libraries. The ceiling is ten; the selection is not padded. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Debian popcon installations of each library's `-dev` package(s) (`by_inst`), captured 2026-11-17 ([snapshot](registry-snapshot.json)). The search is a bounded comparison of four C++ XML parser libraries: tinyxml2, pugixml, Xerces-C++ and libxml++.

| Rank | Library | Release | Dev package installs | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [Xerces-C++](https://xerces.apache.org/xerces-c/) | 3.3.0 | 2,676 (`libxerces-c-dev`) | XML 1.0 + Namespaces from a memory buffer into a DOM, non-validating | Apache Xerces-C++ scanner (IGXMLScanner) |
| 2 | [pugixml](https://pugixml.org/) | 1.16 | 1,503 (`libpugixml-dev`) | XML 1.0 from a memory buffer into a DOM; namespaces resolved by the adapter, not the library | pugixml's own single-file parser |
| 3 | [TinyXML2](https://github.com/leethomason/tinyxml2) | 11.0.0 | 487 (`libtinyxml2-dev`) | XML from a length-bounded memory buffer into a DOM; namespaces resolved by the adapter | TinyXML2 own in-memory parser |
| 4 | [libxml++](https://libxmlplusplus.github.io/libxmlplusplus/) | 5.6.1 | 275 (three ABI `-dev` packages) | XML 1.0 + Namespaces from a memory buffer into a DOM, non-validating | wraps libxml2 C parser |

All four paths give the same structure on the catalog control. Xerces-C++, pugixml, and libxml++ also pass the shared order control; TinyXML2 rejects its processing instruction, so the TinyXML2 path uses a second valid order control with only that instruction removed. Both pugixml and TinyXML2 preserve qualified names; adapter code resolves namespaces. libxml++ delegates actual parsing to libxml2. Its Docker build instruments the wrapper and the pinned libxml2 source; a parser-only probe shows stable, input-dependent AFL++ feedback and different covered `parser.c` lines across the two valid controls.

Xerces-C++ uses its own scanner. Its [parser-only probe](../../../projects/xml/cpp/xerces_c/parser-probe.cpp) calls `XercesDOMParser::parse` without DOM traversal or result formatting; the two valid controls differ by 274 stable scanner source lines and 473 repeat-stable AFL++ tuples ([feedback receipt](../../../fuzzing/afl-native/xml/cpp/xerces_c/differential.json)). The full harness separately checks the namespace-aware tree output.

## Standard API (unranked)

None. The ISO C++ working draft and cppreference's header index contain no XML header ([evidence](standard.json)).

## The metric is close

Homebrew install-on-request (365 days) orders the four libraries differently: tinyxml2 1,757, pugixml 1,270, Xerces-C++ 1,209, libxml++ 461. Debian dev installs, the one primary metric, put Xerces-C++ first by a wide margin (2,676 vs 1,503 for pugixml) and pugixml second, ahead of tinyxml2 (487). On Homebrew, tinyxml2 would lead and Xerces-C++ would be third; that order is a caveat, not a second ranking. The 275 libxml++ dev installations sum `libxml++2.6-dev` (266), `libxml++-4.0-dev` (2), and `libxml++-5.0-dev` (7). Only the last matches the verified ABI-5 release family. Homebrew's 461 corresponds to its older 2.42.4 formula. Source-level popcon is not used: libxml++2.6's 79,794 is a runtime package pulled in by dependents, and 79,361 of those installs show no recent file access.

## Search limit

The bounded search compared only these four named, format-specific C++ XML libraries. Other C++ XML packages may exist and their adoption remains unmeasured here. The two small valid controls do not establish complete XML 1.0, DTD/entity, encoding, or malformed-input behavior. No standard-library XML API was found in the official inventory.

Qt XML, Boost.PropertyTree and POCO XML are parts of larger frameworks and are not ranked by whole-framework installs.
