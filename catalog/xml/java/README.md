# XML / Java — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 1 verified standard APIs, 10 verified Docker harnesses.

Ten third-party XML package paths are verified and runnable, reaching this cell's ceiling without padding: Jackson XML, Xerces2-J, Woodstox, dom4j, XMLBeans, JDOM2, Aalto, XOM, XPP3, and kXML2. Xerces2-J, Woodstox, Aalto, XPP3, and kXML2 are five independent tokenizer/parser families. Jackson XML projects Woodstox StAX events into Jackson tokens; dom4j, XMLBeans, JDOM2, and XOM build distinct trees over the OpenJDK Xerces SAX fork. Each wrapper has own source coverage and stable parser-derived AFL++ feedback, while underlying parser coverage is reported separately. The standard javax.xml.parsers path is counted separately and shares the Xerces2-J family. Four documentation leads remain unresolved, including legacy dom4j:dom4j; it is not counted beside org.dom4j:dom4j. Maven Central search is bounded to 100 hits per query (345 unique hits); deps.dev summed direct dependents measure package adoption, not XML-specific use or independent tokenizer families. Two small UTF-8 XML 1.0 controls without DOCTYPE do not establish DTD, external-entity, schema, non-UTF-8, or XML 1.1 behavior. kXML2 control and differential results are in its project-scoped receipt and the shared XML aggregates.

[Ranking and search limits](../../../data/java/xml/ranking.md) · [Standard API inventory](../../../data/java/xml/standard.json)

## Third-party parsers

- [jackson-dataformat-xml](jackson-dataformat-xml/README.md) — verified Docker harness · [source repository](<https://github.com/FasterXML/jackson-dataformat-xml>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml.jackson.dataformat/jackson-dataformat-xml>)
- [xercesImpl](xercesimpl/README.md) — verified Docker harness · [Maven Central](<https://central.sonatype.com/artifact/xerces/xercesImpl>)
- [woodstox-core](woodstox-core/README.md) — verified Docker harness · [source repository](<https://github.com/FasterXML/woodstox>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml.woodstox/woodstox-core>)
- [dom4j](dom4j/README.md) — verified Docker harness · [source repository](<https://github.com/dom4j/dom4j>) · [Maven Central](<https://central.sonatype.com/artifact/org.dom4j/dom4j>)
- [xmlbeans](xmlbeans/README.md) — verified Docker harness · [Maven Central](<https://central.sonatype.com/artifact/org.apache.xmlbeans/xmlbeans>)
- [jdom2](jdom2/README.md) — verified Docker harness · [source repository](<https://github.com/hunterhacker/jdom>) · [Maven Central](<https://central.sonatype.com/artifact/org.jdom/jdom2>)
- [aalto-xml](aalto-xml/README.md) — verified Docker harness · [source repository](<https://github.com/FasterXML/aalto-xml>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml/aalto-xml>)
- [xom](xom/README.md) — verified Docker harness · [source repository](<https://github.com/elharo/xom>) · [Maven Central](<https://central.sonatype.com/artifact/xom/xom>)
- [xpp3](xpp3/README.md) — verified Docker harness · [Maven Central](<https://central.sonatype.com/artifact/xpp3/xpp3>)
- [kxml2](kxml2/README.md) — verified Docker harness · [Maven Central](<https://central.sonatype.com/artifact/net.sf.kxml/kxml2>)

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
