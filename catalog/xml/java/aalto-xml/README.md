# aalto-xml — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.4.0`
- **Upstream:** [source repository](<https://github.com/FasterXML/aalto-xml>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml/aalto-xml>)
- **License:** Apache-2.0
- **Parser family:** Aalto independent StAX tokenizer/parser
- **Local input API:** `new com.fasterxml.aalto.stax.InputFactoryImpl().createXMLStreamReader(local InputStream); iterate XMLStreamReader.next()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/fasterxml/aalto-xml/1.4.0/aalto-xml-1.4.0-sources.jar>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/java/xml/parsers.json) · [control result](../../../../data/java/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "version=1",
    "id=a1",
    "{urn:parsarium:catalog}lang=es",
    "id=b2"
  ],
  "elements": [
    "{urn:parsarium:catalog}catalog",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}name",
    "{urn:parsarium:item}note"
  ],
  "max_depth": 3,
  "namespace_declarations": 2,
  "namespaces": [
    "urn:parsarium:catalog",
    "urn:parsarium:item"
  ],
  "root": "{urn:parsarium:catalog}catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml java aalto_xml
python3 parsarium.py run xml java aalto_xml controls/xml/catalog-ns.xml
```
