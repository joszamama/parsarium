# github.com/vmware/govmomi/vim25/xml — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.56.2`
- **License:** Apache-2.0, BSD-3-Clause
- **Parser family:** govmomi/vim25/xml fork of Go encoding/xml tokenizer
- **Local input API:** `xml.NewDecoder(io.Reader).Token() over a local byte stream, using the govmomi/vim25/xml package`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/vmware/govmomi/vim25/xml@v0.56.2#NewDecoder>)
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
python3 parsarium.py build xml go github_com_vmware_govmomi_vim25_xml
python3 parsarium.py run xml go github_com_vmware_govmomi_vim25_xml controls/xml/catalog-ns.xml
```
