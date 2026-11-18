# github.com/lestrrat-go/helium — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.11.0`
- **Upstream:** [source repository](<https://github.com/lestrrat-go/helium>) · [pkg.go.dev](<https://pkg.go.dev/github.com/lestrrat-go/helium>)
- **License:** MIT
- **Parser family:** helium pure-Go XML parser (libxml2-style port; independent of encoding/xml)
- **Local input API:** `helium.NewParser().Parse(context.Context, []byte) (*Document, error) with default settings; Document.DocumentElement() DOM walk over Element.URI/LocalName, Element.Namespaces, Element.Attributes (Attribute.URI/LocalName/Value) and FirstChild/NextSibling text, CDATA, comment and PI nodes`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/lestrrat-go/helium@v0.11.0#Parser.Parse>)
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
python3 parsarium.py build xml go github_com_lestrrat_go_helium
python3 parsarium.py run xml go github_com_lestrrat_go_helium controls/xml/catalog-ns.xml
```
