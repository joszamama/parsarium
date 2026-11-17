# github.com/beevik/etree — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.8.1`
- **License:** BSD-2-Clause
- **Parser family:** etree element tree over Go encoding/xml Decoder tokenizer
- **Local input API:** `etree.NewDocument().ReadFromBytes([]byte); Element.Child walk; Element.NamespaceURI(); Attr.NamespaceURI()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/beevik/etree@v1.8.1#Document.ReadFromBytes>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/go/xml/parsers.json) · [control result](../../../../data/go/xml/verification.json)

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
python3 parsarium.py build xml go github_com_beevik_etree
python3 parsarium.py run xml go github_com_beevik_etree controls/xml/catalog-ns.xml
```
