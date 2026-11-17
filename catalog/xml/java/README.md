# XML / Java — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 1 verified standard APIs, 4 verified Docker harnesses.

Pilot cell: xerces:xercesImpl 2.12.2 (2,474 deps.dev summed direct dependents), woodstox-core 7.3.0 (1,874), org.dom4j:dom4j 2.2.0 (1,434), and aalto-xml 1.4.0 (559) are four verified third-party paths with direct local stream APIs, exact namespace-aware output on two valid controls, JaCoCo parser-package source lines, and stable input-dependent AFL++ feedback. Xerces, Woodstox, and Aalto are independent parser engines; dom4j is a wrapper path whose SAXReader builds a tree over the default JAXP SAX parser (the OpenJDK java.xml Xerces fork), so it shares the Apache Xerces2-J family and its AFL++ feedback covers dom4j tree-building lines only. The standard javax.xml.parsers path runs the same OpenJDK Xerces fork and is counted separately. Jackson XML, jsoup, and XStream remain non-parser-engine leads; JDOM delegates to JAXP SAX implementations. 9 documentation leads remain unresolved in leads.json, including the legacy dom4j:dom4j coordinate, which is not counted beside org.dom4j:dom4j. Maven Central search is relevance-ranked, not an adoption ranking; deps.dev metrics are summed per release and may count a dependent repeatedly. These small UTF-8 controls without DOCTYPE do not establish DTD, external-entity, schema, non-UTF-8, or XML 1.1 behavior.

[Ranking and search limits](../../../data/java/xml/ranking.md) · [Standard API inventory](../../../data/java/xml/standard.json)

## Third-party parsers

- [xercesImpl](xercesimpl/README.md) — verified Docker harness
- [woodstox-core](woodstox-core/README.md) — verified Docker harness
- [dom4j](dom4j/README.md) — verified Docker harness
- [aalto-xml](aalto-xml/README.md) — verified Docker harness

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
