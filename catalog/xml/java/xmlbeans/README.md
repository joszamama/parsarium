# xmlbeans — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `5.4.1`
- **Upstream:** [Maven Central](<https://central.sonatype.com/artifact/org.apache.xmlbeans/xmlbeans>)
- **License:** Apache-2.0
- **Parser family:** XMLBeans SAX-to-cursor tree over OpenJDK Xerces2-J fork
- **Local input API:** `XmlObject.Factory.parse(Files.newInputStream(local Path)); XmlObject.newCursor() traverses XML infoset`
- **Documentation:** [API reference](<https://xmlbeans.apache.org/docs/5.0.0/org/apache/xmlbeans/XmlObject.html>)
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
python3 parsarium.py build xml java xmlbeans
python3 parsarium.py run xml java xmlbeans controls/xml/catalog-ns.xml
```
