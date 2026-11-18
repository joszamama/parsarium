# github.com/moovweb/gokogiri/xml — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20180713195410-a1a828153468`
- **Upstream:** [source repository](<https://github.com/moovweb/gokogiri>) · [pkg.go.dev](<https://pkg.go.dev/github.com/moovweb/gokogiri/xml>)
- **License:** MIT
- **Parser family:** gokogiri Go cgo DOM binding over native libxml2 2.15.4
- **Local input API:** `xml.Parse(content []byte, inEncoding []byte, url []byte, options ParseOption, outEncoding []byte) (*XmlDocument, error); Root() and DOM node APIs`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/moovweb/gokogiri/xml@v0.0.0-20180713195410-a1a828153468#Parse>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/go/xml/parsers.json) · [control result](../../../../data/go/xml/verification.json)

## Observed control result

```json
{
  "root": "{urn:parsarium:catalog}catalog",
  "elements": [
    "{urn:parsarium:catalog}catalog",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}name",
    "{urn:parsarium:item}note"
  ],
  "attributes": [
    "version=1",
    "id=a1",
    "{urn:parsarium:catalog}lang=es",
    "id=b2"
  ],
  "namespaces": [
    "urn:parsarium:catalog",
    "urn:parsarium:item"
  ],
  "namespace_declarations": 2,
  "max_depth": 3,
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml go github_com_moovweb_gokogiri
python3 parsarium.py run xml go github_com_moovweb_gokogiri controls/xml/catalog-ns.xml
```
