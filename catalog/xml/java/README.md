# XML / Java — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 1 verified standard API, 10 verified Docker harnesses.

Ten third-party XML package paths are verified and runnable, reaching this cell's ceiling without padding: Jackson XML, Xerces2-J, Woodstox, dom4j, XMLBeans, JDOM2, Aalto, XOM, XPP3, and kXML2. Xerces2-J, Woodstox, Aalto, XPP3, and kXML2 are five independent tokenizer/parser families. Jackson XML projects Woodstox StAX events into Jackson tokens; dom4j, XMLBeans, JDOM2, and XOM build distinct trees over the OpenJDK Xerces SAX fork. Each wrapper has own source coverage and stable parser-derived AFL++ feedback, while underlying parser coverage is reported separately. The standard javax.xml.parsers path is counted separately and shares the Xerces2-J family. Four documentation leads remain unresolved, including legacy dom4j:dom4j; it is not counted beside org.dom4j:dom4j. Maven Central search is bounded to 100 hits per query (345 unique hits); deps.dev summed direct dependents measure package adoption, not XML-specific use or independent tokenizer families. Two small UTF-8 XML 1.0 controls without DOCTYPE do not establish DTD, external-entity, schema, non-UTF-8, or XML 1.1 behavior. kXML2 control and differential results are in project-scoped receipts pending shared XML aggregate refresh.

[Ranking and search limits](../../../data/java/xml/ranking.md) · [Standard API inventory](../../../data/java/xml/standard.json)

## Third-party parsers

- [jackson-dataformat-xml](jackson-dataformat-xml/README.md) — verified Docker harness
- [xercesImpl](xercesimpl/README.md) — verified Docker harness
- [woodstox-core](woodstox-core/README.md) — verified Docker harness
- [dom4j](dom4j/README.md) — verified Docker harness
- [xmlbeans](xmlbeans/README.md) — verified Docker harness
- [jdom2](jdom2/README.md) — verified Docker harness
- [aalto-xml](aalto-xml/README.md) — verified Docker harness
- [xom](xom/README.md) — verified Docker harness
- [xpp3](xpp3/README.md) — verified Docker harness
- [kxml2](kxml2/README.md) — verified Docker harness

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
