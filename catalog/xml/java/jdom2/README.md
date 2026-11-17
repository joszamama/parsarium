# jdom2 — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.0.6.1`
- **License:** JDOM license
- **Parser family:** JDOM2 SAXHandler/tree over OpenJDK Xerces2-J fork
- **Local input API:** `new SAXBuilder().build(Files.newInputStream(local Path)) into JDOM Document`
- **Documentation:** [API reference](<https://www.jdom.org/docs/apidocs/org/jdom2/input/SAXBuilder.html>)
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
python3 parsarium.py build xml java jdom2
python3 parsarium.py run xml java jdom2 controls/xml/catalog-ns.xml
```
