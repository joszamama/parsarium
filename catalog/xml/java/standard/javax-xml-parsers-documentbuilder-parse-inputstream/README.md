# javax.xml.parsers.DocumentBuilder.parse(InputStream) — XML / Java

**Pilot / incomplete format cell.**

- **Runtime:** Eclipse Temurin OpenJDK 25.0.5+8 linux/arm64 java.xml
- **Parser family:** Apache Xerces2-J (OpenJDK java.xml internal fork)
- **Official documentation:** [reference](https://docs.oracle.com/en/java/javase/25/docs/api/java.xml/javax/xml/parsers/DocumentBuilder.html#parse(java.io.InputStream))
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../../controls/xml/catalog-ns.xml)
- **Inventory:** [standard API record](../../../../../data/java/xml/standard.json) · [saved result](../../../../../projects/xml/java/jdk_documentbuilder/verification.json)

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
python3 parsarium.py build xml java jdk_documentbuilder
python3 parsarium.py run xml java jdk_documentbuilder controls/xml/catalog-ns.xml
```
