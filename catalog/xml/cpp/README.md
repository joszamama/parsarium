# XML / C++ — pilot

**Status:** pilot_seven_selected_search_bounded; incomplete. 7 verified third-party paths, 0 verified standard APIs, 7 verified Docker harnesses.

Six C++ XML paths pass the namespace-aware catalog control, and cxxtools passes both controls as a raw-name path, with source coverage and AFL++ feedback. Xerces-C++, pugixml, TinyXML, libxml++, cxxtools and RapidXML pass the shared second valid control; TinyXML2 uses a no-processing-instruction variant because it rejects that instruction, while RapidXML's default flags skip it. libxml++ parser-only feedback and native libxml2 parser.c lines are repeatable and input-dependent. The bounded search covered five named format-specific libraries and, on 2026-11-18, a Debian by_inst lookup of C++ XML -dev and framework packages in the same snapshot. TinyXML 2.6.2 (libtinyxml-dev 533) was added from it: a separate Debian source and code base from TinyXML2 (51 of 1,698 normalized non-trivial parser lines, 3.0%, match tinyxml2.cpp in sequence), with namespaces resolved by the adapter as for TinyXML2, pugixml and RapidXML. The pinned upstream 2.6.2 omits Debian's CVE and entity-encoding patches, which concern malformed input and output. Boost.PropertyTree is excluded (84.2% in-sequence overlap of its embedded rapidxml.hpp with RapidXML 1.13, and a framework-wide package); Xalan-C++, XQilla, CodeSynthesis XSD and XMLTooling run over Xerces-C++; gSOAP (95) and Arabica (2) stay unresolved, Qt XML DOM and libstudxml have no qualifying metric. Other C++ XML packages remain unmeasured. Homebrew install-on-request orders the first three differently and its libxml++ formula is an older ABI; RapidXML has no Homebrew formula. The libxml++ 275 Debian dev installs sum three ABIs, while its matching ABI-5 package has seven. RapidXML's 17 librapidxml-dev installations, none with recent use, are a weak adoption signal and exclude vendored or Boost-embedded copies. Two small valid UTF-8 controls cannot establish complete XML 1.0, DTD/entity, encoding or malformed-input behavior. cxxtools 3.0.0 (libcxxtools-dev 42) has its own XmlReader state machine, but XmlReader never fills the StartElement NamespaceContext, so it is measured as a raw-name path (names as written, xmlns as attributes) against the expat non-namespace oracle used for the C raw-name paths; its package count reflects a general C++ utility library, not XML-specific use. The cell stays at seven: the remaining Debian C++ XML packages are Xerces-C++ or libxml2 dependants, wrappers or code generators, gSOAP and Arabica are unresolved, and Qt XML, POCO XML and libstudxml lack a qualifying metric.

[Ranking and search limits](../../../data/cpp/xml/ranking.md) · [Standard API inventory](../../../data/cpp/xml/standard.json)

## Third-party parsers

- [xerces-c](xerces-c/README.md) — verified Docker harness
- [pugixml](pugixml/README.md) — verified Docker harness
- [tinyxml](tinyxml/README.md) — verified Docker harness
- [tinyxml2](tinyxml2/README.md) — verified Docker harness
- [libxml++](libxml/README.md) — verified Docker harness
- [cxxtools](cxxtools/README.md) — verified Docker harness
- [rapidxml](rapidxml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
