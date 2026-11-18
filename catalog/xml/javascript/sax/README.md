# sax — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.6.1`
- **Upstream:** [source repository](<https://github.com/isaacs/sax-js>) · [npm](<https://www.npmjs.com/package/sax>)
- **License:** BlueOak-1.0.0
- **Parser family:** sax-js hand-written strict XML state machine
- **Local input API:** `sax.parser(true, {xmlns: true, strictEntities: true}).write(string).close() after strict UTF-8 TextDecoder of local bytes; documented createStream(true, {xmlns: true}) also accepts a local file stream`
- **Documentation:** [API reference](<https://github.com/isaacs/sax-js/blob/v1.6.1/README.md>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/javascript/xml/parsers.json) · [control result](../../../../data/javascript/xml/verification.json)

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
python3 parsarium.py build xml javascript sax
python3 parsarium.py run xml javascript sax controls/xml/catalog-ns.xml
```
