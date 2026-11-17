# dom4j — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.2.0`
- **License:** BSD-3-Clause
- **Parser family:** dom4j SAX tree builder over the JAXP default SAX parser (OpenJDK java.xml Xerces2-J fork)
- **Local input API:** `org.dom4j.io.SAXReader.createDefault().read(local InputStream) returns an org.dom4j.Document; walk Element.content()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/dom4j/dom4j/2.2.0/dom4j-2.2.0-sources.jar>)
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
python3 parsarium.py build xml java dom4j
python3 parsarium.py run xml java dom4j controls/xml/catalog-ns.xml
```
