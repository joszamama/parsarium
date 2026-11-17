# aalto-xml — XML / Java

**Verified path in an incomplete format cell.**

- **Pinned release:** `com.fasterxml:aalto-xml:1.4.0` (Apache-2.0)
- **Parser family:** Aalto’s independent StAX reader and UTF-8 scanners
- **Local input API:** `InputFactoryImpl.createXMLStreamReader(InputStream)` over a local byte stream
- **Documentation:** [pinned release source](https://repo.maven.apache.org/maven2/com/fasterxml/aalto-xml/1.4.0/aalto-xml-1.4.0-sources.jar), `InputFactoryImpl.java` lines 172–176
- **Valid controls:** [catalog with namespaces](../../../../controls/xml/catalog-ns.xml), [order with default namespace](../../../../controls/xml/order-default-ns.xml)
- **Evidence:** [parser record](../../../../data/java/xml/parsers.json), [control result](../../../../data/java/xml/verification.json), [project and commands](../../../../projects/xml/java/aalto_xml/README.md)

The controls produce the expected namespace-aware element and attribute names, decoded text, and depth. JaCoCo covered 1,427 Aalto source lines. AFL++ feedback was stable on repeated valid inputs and differed on the second control. The controls establish only this tested XML 1.0 subset.
