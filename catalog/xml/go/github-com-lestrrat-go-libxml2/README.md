# github.com/lestrrat-go/libxml2 — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20260709020957-3f0f7bd60b63`
- **License:** MIT
- **Parser family:** lestrrat-go/libxml2 Go cgo DOM binding over native libxml2 2.15.4
- **Local input API:** `libxml2.Parse([]byte, ...parser.Option) (types.Document, error) with parser.XMLParseNoNet; Document.DocumentElement() and Element NamespaceURI/LocalName, GetNamespaces, Attributes, FirstChild/NextSibling, NodeValue`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/lestrrat-go/libxml2@v0.0.0-20260709020957-3f0f7bd60b63#Parse>)
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
python3 parsarium.py build xml go github_com_lestrrat_go_libxml2
python3 parsarium.py run xml go github_com_lestrrat_go_libxml2 controls/xml/catalog-ns.xml
```
