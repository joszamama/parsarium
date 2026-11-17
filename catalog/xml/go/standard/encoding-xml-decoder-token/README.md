# encoding/xml.Decoder.Token() — XML / Go

**Pilot / incomplete format cell.**

- **Runtime:** Go 1.27.1 linux/arm64 standard library
- **Parser family:** Go encoding/xml Decoder tokenizer
- **Official documentation:** [reference](https://pkg.go.dev/encoding/xml@go1.27.1#Decoder.Token)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../../controls/xml/catalog-ns.xml)
- **Inventory:** [standard API record](../../../../../data/go/xml/standard.json) · [saved result](../../../../../projects/xml/go/stdlib_decoder/verification.json)

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
python3 parsarium.py build xml go stdlib_decoder
python3 parsarium.py run xml go stdlib_decoder controls/xml/catalog-ns.xml
```
