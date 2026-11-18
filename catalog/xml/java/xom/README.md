# xom — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.4.6`
- **Upstream:** [source repository](<https://github.com/elharo/xom>) · [Maven Central](<https://central.sonatype.com/artifact/xom/xom>)
- **License:** LGPL-2.1
- **Parser family:** XOM Builder/tree over OpenJDK Xerces2-J fork
- **Local input API:** `new nu.xom.Builder().build(Files.newInputStream(local Path)) into XOM Document`
- **Documentation:** [API reference](<https://xom.nu/apidocs/nu/xom/Builder.html>)
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
python3 parsarium.py build xml java xom
python3 parsarium.py run xml java xom controls/xml/catalog-ns.xml
```
