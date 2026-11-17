# kxml2 — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.3.0`
- **License:** BSD-style (org.kxml2 parser); public domain (bundled XmlPull API)
- **Parser family:** kXML2 KXmlParser independent XML pull tokenizer
- **Local input API:** `new org.kxml2.io.KXmlParser(); setFeature(FEATURE_PROCESS_NAMESPACES, true); setInput(Files.newInputStream(local Path), null); next() until END_DOCUMENT`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/net/sf/kxml/kxml2/2.3.0/kxml2-2.3.0-sources.jar>)
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
python3 parsarium.py build xml java kxml2
python3 parsarium.py run xml java kxml2 controls/xml/catalog-ns.xml
```
