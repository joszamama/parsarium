# XML / Java — pilot

**Status:** pilot_nine_selected_search_bounded; incomplete. 9 verified third-party paths, 1 verified standard APIs, 9 verified Docker harnesses.

Nine third-party XML package paths are verified and runnable: Jackson XML, Xerces2-J, Woodstox, dom4j, XMLBeans, JDOM2, Aalto, XOM, and XPP3. Xerces2-J, Woodstox, Aalto, and XPP3 are independent tokenizer/parser engines. Jackson XML projects Woodstox StAX into Jackson tokens; dom4j, XMLBeans, JDOM2, and XOM build distinct trees over the OpenJDK Xerces SAX fork. Each wrapper has its own source coverage and stable parser-derived AFL++ feedback, while underlying tokenizer coverage is reported separately. The standard javax.xml.parsers path shares the Xerces2-J family. Five documentation leads remain unresolved, including legacy dom4j:dom4j; it is not counted beside org.dom4j:dom4j. Maven Central search is bounded to 100 hits per query (345 unique hits); deps.dev summed direct dependents measure package adoption, not XML-specific use or independent tokenizer families. Two small UTF-8 XML 1.0 controls without DOCTYPE do not establish DTD, external-entity, schema, non-UTF-8, or XML 1.1 behavior. XOM and XPP3 control and differential results are in their project-scoped receipts and shared XML aggregates.

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

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
