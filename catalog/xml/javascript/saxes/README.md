# saxes — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `6.0.0`
- **Upstream:** [source repository](<https://github.com/lddubeau/saxes>) · [npm](<https://www.npmjs.com/package/saxes>)
- **License:** ISC
- **Parser family:** saxes hand-written XML 1.0 + Namespaces state machine (sax-js fork)
- **Local input API:** `new SaxesParser({xmlns: true}); on('opentag'|'closetag'|'text'|'cdata'|'comment'|'processinginstruction'|'error'); write(string).close() after strict UTF-8 TextDecoder of local bytes`
- **Documentation:** [API reference](<https://github.com/lddubeau/saxes/blob/v6.0.0/README.md>)
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
python3 parsarium.py build xml javascript saxes
python3 parsarium.py run xml javascript saxes controls/xml/catalog-ns.xml
```
