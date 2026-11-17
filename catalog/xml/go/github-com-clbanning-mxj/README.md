# github.com/clbanning/mxj — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.8.4`
- **License:** MIT, with BSD-3-Clause Go Authors notice
- **Parser family:** mxj map conversion over Go encoding/xml Decoder tokenizer
- **Local input API:** `mxj.NewMapXml([]byte) and mxj.NewMapXmlReader(io.Reader), each returning mxj.Map (map[string]interface{}); the harness requires both maps to agree and walks the map keys`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/clbanning/mxj@v1.8.4#NewMapXml>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/go/xml/parsers.json) · [control result](../../../../data/go/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "catalog/-c=urn:parsarium:catalog",
    "catalog/-version=1",
    "catalog/-xmlns=urn:parsarium:item",
    "catalog/item[0]/-id=a1",
    "catalog/item[0]/-lang=es",
    "catalog/item[1]/-id=b2"
  ],
  "elements": [
    "catalog",
    "catalog/item[0]",
    "catalog/item[1]",
    "catalog/item[1]/name",
    "catalog/item[1]/note"
  ],
  "empty_elements": [],
  "lists": [
    "catalog/item=2"
  ],
  "max_depth": 3,
  "root": "catalog",
  "text": [
    "catalog/item[0]/#text=Café & té",
    "catalog/item[1]/name=Zürich <HQ>",
    "catalog/item[1]/note=x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml go github_com_clbanning_mxj
python3 parsarium.py run xml go github_com_clbanning_mxj controls/xml/catalog-ns.xml
```
