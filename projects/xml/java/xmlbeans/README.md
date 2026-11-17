# XMLBeans — XML / Java

Pinned `org.apache.xmlbeans:xmlbeans:5.4.1` reads local XML with `XmlObject.Factory.parse(InputStream)`. Its cursor exposes expanded element and attribute names, namespace declarations, decoded text, and structure. The XMLBeans SAX-to-tree layer delegates lexical XML parsing to the OpenJDK `java.xml` Xerces fork through JAXP; this release does not bundle a Piccolo tokenizer. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json) · [API and family evidence](../../../../catalog/xml/java/xmlbeans/README.md).

```sh
python3 parsarium.py build xml java xmlbeans
python3 parsarium.py run xml java xmlbeans controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xmlbeans CORPUS_DIR runs/xml-xmlbeans-replay
python3 parsarium.py afl build xml java xmlbeans
python3 parsarium.py afl prepare xml java xmlbeans runs/xml-xmlbeans-afl
```

`afl prepare` seeds a run; it does not start a campaign. The two valid controls cover a narrow UTF-8 XML 1.0 subset without DOCTYPE.
