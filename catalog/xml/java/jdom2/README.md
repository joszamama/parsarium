# JDOM2 — XML / Java

**Pilot / incomplete format cell.** This path passed two valid namespace-aware XML controls.

- **Pinned release:** `org.jdom:jdom2:2.0.6.1`; its three Maven dependencies are optional for this SAXBuilder path. [JAR, source, POM, and OpenJDK hashes](../../../../projects/xml/java/jdom2/source-lock.json).
- **License:** the permissive JDOM license in the release JAR `META-INF/LICENSE.txt` and [Maven POM](https://repo.maven.apache.org/maven2/org/jdom/jdom2/2.0.6.1/jdom2-2.0.6.1.pom); it is Apache-like but is recorded under its own name.
- **Local API:** `new SAXBuilder().build(InputStream)` to a JDOM `Document`. [Official API reference](https://www.jdom.org/docs/apidocs/org/jdom2/input/SAXBuilder.html).
- **Family:** JDOM2 `SAXHandler`/tree over a JAXP SAX parser (OpenJDK `java.xml` Xerces fork in this runtime). JDOM2 is a format-specific package path with its own tree implementation, and shares the underlying tokenizer family with dom4j and the standard API.
- **Valid controls:** [namespace catalog](../../../../controls/xml/catalog-ns.xml) and [default namespace order](../../../../controls/xml/order-default-ns.xml). Expanded names, attributes, declarations, depth, and decoded text match the independent [expat oracle](../../../../controls/xml/check_controls.py).
- **Evidence:** [parser record](../../../../data/java/xml/parsers.json), [control receipt](../../../../projects/xml/java/jdom2/verification.json), [AFL feedback](../../../../data/java/xml/afl-feedback.json).

JaCoCo covered 734 JDOM2 source lines (`SAXBuilder`, `SAXHandler`, factory and tree classes) and separately 3,549 underlying OpenJDK Xerces lines. Three repeated valid probes per control were identical; the controls differed by 146 JDOM2 source features and 144 AFL++ tuples. The 968 deps.dev summed direct dependents measure Maven coordinate adoption, not XML-specific use or an independent tokenizer.

```sh
python3 parsarium.py build xml java jdom2
python3 parsarium.py run xml java jdom2 controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml java jdom2
python3 parsarium.py afl prepare xml java jdom2 runs/xml-jdom2-afl
```
