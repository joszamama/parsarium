# JDOM2 — XML / Java

Pinned `org.jdom:jdom2:2.0.6.1` reads local XML through `SAXBuilder.build(InputStream)` and constructs a namespace-aware JDOM tree. Its `SAXHandler` and factory build the tree from the default JAXP SAX reader; in the pinned runtime, that reader is the OpenJDK Xerces fork. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json) · [API and family evidence](../../../../catalog/xml/java/jdom2/README.md).

```sh
python3 parsarium.py build xml java jdom2
python3 parsarium.py run xml java jdom2 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java jdom2 CORPUS_DIR runs/xml-jdom2-replay
python3 parsarium.py afl build xml java jdom2
python3 parsarium.py afl prepare xml java jdom2 runs/xml-jdom2-afl
```

`afl prepare` seeds a run; it does not start a campaign. The two valid controls cover a narrow UTF-8 XML 1.0 subset without DOCTYPE.
