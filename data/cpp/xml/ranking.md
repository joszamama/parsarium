# C++ × XML: selected parsers (pilot)

1 control-verified third-party path selected. The ceiling is ten; this pilot builds only the highest-adoption C++ XML parser and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Debian popcon installations of each library's `-dev` package(s) (`by_inst`), captured 2026-11-17 ([snapshot](registry-snapshot.json)). The search is a bounded comparison of four C++ XML parser libraries: tinyxml2, pugixml, Xerces-C++ and libxml++.

| Rank | Library | Release | Dev package installs | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [Xerces-C++](https://xerces.apache.org/xerces-c/) | 3.3.0 | 2,676 (`libxerces-c-dev`) | XML 1.0 + Namespaces from a memory buffer into a DOM, non-validating | Apache Xerces-C++ scanner (IGXMLScanner) |

## Standard API (unranked)

None. The ISO C++ working draft and cppreference's header index contain no XML header ([evidence](standard.json)).

## The metric is close

Homebrew install-on-request (365 days) orders the four libraries differently: tinyxml2 1,757, pugixml 1,270, Xerces-C++ 1,209, libxml++ 461. Debian dev installs put Xerces-C++ first by a wide margin (2,676 vs 1,503 for pugixml), so it is the selected path. Source-level popcon is not used: libxml++2.6's 79,794 is a runtime package pulled in by dependents, and 79,361 of those installs show no recent file access.

## Lead log

Numeric leads, not verified and not selected.

| Lead | Dev package installs | Homebrew on request (365d) | Status |
| --- | ---: | ---: | --- |
| [pugixml](https://github.com/zeux/pugixml) | 1,503 | 1,270 | no namespace processing; not run |
| [tinyxml2](https://github.com/leethomason/tinyxml2) | 487 | 1,757 | no namespace processing; not run |
| [libxml++](https://github.com/libxmlplusplus/libxmlplusplus) | 275 | 461 | wraps the libxml2 C parser (libxml2 family); not run |

Qt XML, Boost.PropertyTree and POCO XML are parts of larger frameworks and are not ranked by whole-framework installs.
