# @xmldom/xmldom — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.9.12`
- **License:** MIT
- **Parser family:** xmldom XMLReader tokenizer + DOMHandler DOM builder (jindw/xmldom lineage)
- **Local input API:** `new DOMParser({onError}).parseFromString(text, 'application/xml') on in-memory text from a strict UTF-8 TextDecoder of local bytes; the adapter's onError throws on every warning, error or fatalError; the summary reads the returned Document's namespaceURI/localName/attributes`
- **Documentation:** [API reference](<https://github.com/xmldom/xmldom/blob/0.9.12/readme.md>)
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
python3 parsarium.py build xml javascript xmldom_xmldom
python3 parsarium.py run xml javascript xmldom_xmldom controls/xml/catalog-ns.xml
```
