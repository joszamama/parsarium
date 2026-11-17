# XML / Java — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 1 verified standard APIs, 3 verified Docker harnesses.

Pilot cell: xerces:xercesImpl 2.12.2 (2,474 deps.dev summed direct dependents), woodstox-core 7.3.0 (1,874), and aalto-xml 1.4.0 (559) are three independent third-party XML parser families with direct local stream APIs, exact namespace-aware output on two valid controls, JaCoCo parser-source lines, and stable input-dependent AFL++ feedback. The standard javax.xml.parsers path runs an OpenJDK Xerces fork and is counted separately. Jackson XML, jsoup, and XStream remain non-parser-engine leads; dom4j and JDOM delegate to JAXP SAX implementations. Ten documentation leads remain unresolved in leads.json. Maven Central search is relevance-ranked, not an adoption ranking; deps.dev metrics are summed per release and may count a dependent repeatedly. These small UTF-8 controls without DOCTYPE do not establish DTD, external-entity, schema, non-UTF-8, or XML 1.1 behavior.

[Ranking and search limits](../../../data/java/xml/ranking.md) · [Standard API inventory](../../../data/java/xml/standard.json)

## Third-party parsers

- [xercesImpl](xercesimpl/README.md) — verified Docker harness
- [woodstox-core](woodstox-core/README.md) — verified Docker harness
- [aalto-xml](aalto-xml/README.md) — verified Docker harness

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
