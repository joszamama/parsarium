# github.com/beego/x2j — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20131220205130-a0352aadc542`
- **Upstream:** [source repository](<https://github.com/beego/x2j>) · [pkg.go.dev](<https://pkg.go.dev/github.com/beego/x2j>)
- **License:** BSD-3-Clause
- **Parser family:** x2j map conversion over Go encoding/xml Decoder tokenizer
- **Local input API:** `Primary oracle-matching route: x2j.ToMap(io.Reader) on a local byte stream. The harness also records x2j.Unmarshal([]byte, &map[string]interface{}), ByteDocToMap([]byte), and DocToMap(string) as auxiliary routes; those three agree with one another but alter CDATA whitespace on the first valid control.`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/beego/x2j@v0.0.0-20131220205130-a0352aadc542#ToMap>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/go/xml/parsers.json) · [control result](../../../../data/go/xml/verification.json)

## Observed control result

```json
{
  "bytes": {
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
      "catalog/item[1]/note=x< y"
    ]
  },
  "reader": {
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
      "catalog/#text=3",
      "catalog/item=2"
    ],
    "max_depth": 3,
    "root": "catalog",
    "text": [
      "catalog/#text[0]=\n  ",
      "catalog/#text[1]=\n  ",
      "catalog/#text[2]=\n",
      "catalog/item[0]/#text=Café & té",
      "catalog/item[1]/name=Zürich <HQ>",
      "catalog/item[1]/note=x < y"
    ]
  }
}
```

## Run this target

```sh
python3 parsarium.py build xml go github_com_beego_x2j
python3 parsarium.py run xml go github_com_beego_x2j controls/xml/catalog-ns.xml
```
