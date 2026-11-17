# XML / Java — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 1 verified standard API, 5 verified Docker harnesses.

Five third-party XML package paths are verified and runnable: Jackson XML, Xerces2-J, Woodstox, dom4j, and Aalto. Xerces2-J, Woodstox, and Aalto are independent tokenizer/parser engines. Jackson XML is a format-specific token projection over pinned Woodstox; its own module and the underlying Woodstox parser have separate source coverage. Its ordered token output retains decoded field/value text but omits namespace URIs, root name, comments, processing instructions, and attribute-versus-child origin. dom4j builds a tree over the default JAXP SAX parser (OpenJDK Xerces fork), with dom4j and underlying JDK coverage separately recorded. The standard javax.xml.parsers path is counted separately and shares the Xerces2-J family. Nine documentation leads remain unresolved; legacy dom4j:dom4j is not counted beside org.dom4j:dom4j. Maven Central search is relevance-ranked and bounded to 100 hits per query (345 unique hits); deps.dev sums direct dependents per release and does not measure XML-specific use or independent parser families. Two small UTF-8 XML 1.0 controls without DOCTYPE do not establish DTD, external-entity, schema, non-UTF-8, or XML 1.1 behavior.

[Ranking and search limits](../../../data/java/xml/ranking.md) · [Standard API inventory](../../../data/java/xml/standard.json)

## Third-party parsers

- [jackson-dataformat-xml](jackson-dataformat-xml/README.md) — verified Docker harness
- [xercesImpl](xercesimpl/README.md) — verified Docker harness
- [woodstox-core](woodstox-core/README.md) — verified Docker harness
- [dom4j](dom4j/README.md) — verified Docker harness
- [aalto-xml](aalto-xml/README.md) — verified Docker harness

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
