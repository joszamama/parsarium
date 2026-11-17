# Jackson XML — XML / Java

**Pilot / incomplete format cell.** This path is verified on two valid XML controls.

- **Pinned release:** `com.fasterxml.jackson.dataformat:jackson-dataformat-xml:2.23.0`, with pinned Jackson core/databind/annotations, Woodstox 7.3.0, and StAX2 API 4.3.1. [Hashes](../../../../projects/xml/java/jackson_xml/source-lock.json).
- **License:** Apache-2.0 in the [Jackson base POM](https://repo.maven.apache.org/maven2/com/fasterxml/jackson/jackson-base/2.23.0/jackson-base-2.23.0.pom) and [project README](https://github.com/FasterXML/jackson-dataformat-xml).
- **Local API:** `new XmlFactory(new WstxInputFactory()).createParser(InputStream)` and `nextToken()` to EOF. [Release source](https://repo.maven.apache.org/maven2/com/fasterxml/jackson/dataformat/jackson-dataformat-xml/2.23.0/jackson-dataformat-xml-2.23.0-sources.jar).
- **Family:** Jackson XML token projection over Woodstox StAX. This path shares the underlying Woodstox tokenizer with the selected woodstox-core path; the module has its own `FromXmlParser` and `XmlTokenStream` source.
- **Valid controls:** [namespace catalog](../../../../controls/xml/catalog-ns.xml) and [default namespace order](../../../../controls/xml/order-default-ns.xml).
- **Evidence:** [parser record](../../../../data/java/xml/parsers.json), [control receipt](../../../../projects/xml/java/jackson_xml/verification.json), [AFL feedback](../../../../data/java/xml/afl-feedback.json).

The first control yielded 22 ordered Jackson tokens, including two `item` fields and decoded `Café & té`, `Zürich <HQ>`, and `x < y` values. The second yielded 25 tokens with decoded `A-7`, `12.50 €`, and `say "hi"`. The projection omits namespace URIs, the root element name, comments, processing instructions, and attribute-versus-child origin; these are not claims of XML tree equivalence.

JaCoCo covered 320 own module source lines, including `FromXmlParser` and `XmlTokenStream`, plus 832 underlying Woodstox StAX source lines. Repeated valid controls gave stable parser-source feedback; the second control changed 17 module features and 17 AFL++ tuples. The 25,682 deps.dev summed direct-dependent metric measures Jackson XML package adoption, not an independent XML tokenizer or XML-specific use by each dependent.

```sh
python3 parsarium.py build xml java jackson_xml
python3 parsarium.py run xml java jackson_xml controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml java jackson_xml
python3 parsarium.py afl prepare xml java jackson_xml runs/xml-jackson-xml-afl
```
