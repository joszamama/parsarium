# xpp3 — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.1.4c`
- **License:** Indiana University Extreme! Lab Software License 1.1.1 (parser); public domain (XmlPull API); Apache-1.1 (bundled QName)
- **Parser family:** XPP3 MXParser independent XML pull tokenizer
- **Local input API:** `new org.xmlpull.mxp1.MXParser(); setFeature(FEATURE_PROCESS_NAMESPACES, true); setInput(Files.newInputStream(local Path), null); next() until END_DOCUMENT`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/xpp3/xpp3/1.1.4c/xpp3-1.1.4c-sources.jar>)
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
python3 parsarium.py build xml java xpp3
python3 parsarium.py run xml java xpp3 controls/xml/catalog-ns.xml
```
