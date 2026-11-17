# Jackson XML — XML / Java

Pinned `com.fasterxml.jackson.dataformat:jackson-dataformat-xml:2.23.0` exposes a format-specific `XmlFactory.createParser(InputStream)` path. The adapter uses its `FromXmlParser` and `XmlTokenStream` over pinned Woodstox 7.3.0 StAX. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json).

The observable result is the ordered Jackson token stream, with field names and decoded string values. This projection does not preserve namespace URIs, root name, comments, processing instructions, or whether a field came from an XML attribute or child element. The two controls cover valid UTF-8 XML 1.0 without DOCTYPE; they do not establish broader XML behavior. [API and family evidence](../../../../catalog/xml/java/jackson-dataformat-xml/README.md).

```sh
python3 parsarium.py build xml java jackson_xml
python3 parsarium.py run xml java jackson_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java jackson_xml CORPUS_DIR runs/xml-jackson-xml-replay
python3 parsarium.py afl build xml java jackson_xml
python3 parsarium.py afl prepare xml java jackson_xml runs/xml-jackson-xml-afl
```

`afl prepare` seeds a run; it does not start a campaign.
