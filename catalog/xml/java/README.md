# XML / Java — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 1 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: xerces:xercesImpl 2.12.2 (2,474 deps.dev summed direct dependents) and com.fasterxml.woodstox:woodstox-core 7.3.0 (1,874) are independent third-party parser families with documented local stream APIs, exact namespace-aware structural results on two valid controls, JaCoCo parser-source lines, and stable input-dependent AFL++ feedback. Jackson XML, jsoup, and XStream remain non-parser-engine leads; dom4j and JDOM build trees over a JAXP SAX parser that defaults to the JDK Xerces fork. The standard javax.xml.parsers path runs an OpenJDK Xerces fork and is counted separately. Woodstox feedback is scoped to com.ctc.wstx.sr reader/scanner classes; its symbol-table cache has process-dependent paths and is excluded from the feedback scope. Maven Central text search ranks by relevance, not adoption; deps.dev metrics are summed per release and may count one dependent repeatedly. The small UTF-8 controls without DOCTYPE do not establish DTD, entity, schema, non-UTF-8, or XML 1.1 behavior.

[Ranking and search limits](../../../data/java/xml/ranking.md) · [Standard API inventory](../../../data/java/xml/standard.json)

## Third-party parsers

- [xercesImpl](xercesimpl/README.md) — verified Docker harness
- [woodstox-core](woodstox-core/README.md) — verified Docker harness

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
