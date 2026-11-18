# woodstox-core — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `7.3.0`
- **Upstream:** [source repository](<https://github.com/FasterXML/woodstox>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml.woodstox/woodstox-core>)
- **License:** Apache-2.0
- **Parser family:** Woodstox independent StAX tokenizer/parser
- **Local input API:** `new com.ctc.wstx.stax.WstxInputFactory().createXMLStreamReader(local InputStream), namespace-aware; iterate XMLStreamReader.next()`
- **Documentation:** [API reference](<https://docs.oracle.com/en/java/javase/25/docs/api/java.xml/javax/xml/stream/XMLInputFactory.html#createXMLStreamReader(java.io.InputStream)>)
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
python3 parsarium.py build xml java woodstox_core
python3 parsarium.py run xml java woodstox_core controls/xml/catalog-ns.xml
```
