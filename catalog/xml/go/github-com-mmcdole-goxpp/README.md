# github.com/mmcdole/goxpp — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.3.0`
- **Upstream:** [source repository](<https://github.com/mmcdole/goxpp>) · [pkg.go.dev](<https://pkg.go.dev/github.com/mmcdole/goxpp>)
- **License:** MIT
- **Parser family:** goxpp XML pull cursor over Go encoding/xml Decoder.Token tokenizer
- **Local input API:** `xpp.NewXMLPullParser(io.Reader, true, nil) over a local byte stream, then XMLPullParser.NextToken() events`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/mmcdole/goxpp@v1.3.0#NewXMLPullParser>)
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
python3 parsarium.py build xml go github_com_mmcdole_goxpp
python3 parsarium.py run xml go github_com_mmcdole_goxpp controls/xml/catalog-ns.xml
```
