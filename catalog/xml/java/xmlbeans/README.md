# XMLBeans — XML / Java

**Pilot / incomplete format cell.** This path passed two valid XML controls.

- **Pinned release:** `org.apache.xmlbeans:xmlbeans:5.4.1`, Log4j API and a logging provider, plus the matching OpenJDK 25.0.5 `java.xml` module. [Hashes](../../../../projects/xml/java/xmlbeans/source-lock.json).
- **License:** Apache-2.0 ([release POM](https://repo.maven.apache.org/maven2/org/apache/xmlbeans/xmlbeans/5.4.1/xmlbeans-5.4.1.pom) and source headers).
- **Local API:** `XmlObject.Factory.parse(InputStream)` followed by `XmlObject.newCursor()` to traverse the parsed XML infoset. [Official API reference](https://xmlbeans.apache.org/docs/5.0.0/org/apache/xmlbeans/XmlObject.html) · [cursor reference](https://xmlbeans.apache.org/docs/5.0.0/org/apache/xmlbeans/XmlCursor.html).
- **Family:** XMLBeans SAX-to-cursor tree over the OpenJDK Xerces2-J fork. In 5.4.1, `Locale.parseToXmlObject(InputStream)` uses `SAXHelper.newXMLReader`, which calls JAXP `SAXParserFactory.newInstance()`; this release has no bundled Piccolo tokenizer. [Pinned sources](https://repo.maven.apache.org/maven2/org/apache/xmlbeans/xmlbeans/5.4.1/xmlbeans-5.4.1-sources.jar).
- **Valid controls:** [namespace catalog](../../../../controls/xml/catalog-ns.xml) and [default namespace order](../../../../controls/xml/order-default-ns.xml). Outputs match the independent [expat oracle](../../../../controls/xml/check_controls.py) for expanded names, attributes, declarations, depth, and decoded text.
- **Evidence:** [parser record](../../../../data/java/xml/parsers.json), [control receipt](../../../../projects/xml/java/xmlbeans/verification.json), [AFL feedback](../../../../data/java/xml/afl-feedback.json).

JaCoCo covered 1,004 XMLBeans tree/SAX helper lines and separately 3,733 underlying JDK Xerces lines on the first control. XMLBeans-scoped AFL feedback repeated identically across three probes per valid control; the two controls differed by 90 source features and 89 AFL++ tuples. The 1,433 deps.dev summed direct dependents measure Maven coordinate adoption, not XML-specific use or an independent tokenizer family.

```sh
python3 parsarium.py build xml java xmlbeans
python3 parsarium.py run xml java xmlbeans controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml java xmlbeans
python3 parsarium.py afl prepare xml java xmlbeans runs/xml-xmlbeans-afl
```
