# github.com/go-forks/go-pkg-xmlx — XML / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20151201012946-76f54ee73233`
- **Upstream:** [source repository](<https://github.com/go-forks/go-pkg-xmlx>) · [pkg.go.dev](<https://pkg.go.dev/github.com/go-forks/go-pkg-xmlx>)
- **License:** CC0-1.0
- **Parser family:** go-pkg-xmlx node tree over Go encoding/xml Decoder tokenizer
- **Local input API:** `xmlx.New() then Document.LoadBytes([]byte, nil) (LoadStream over a local byte buffer); Document.Root node tree walk over Node.Type, Node.Name, Node.Attributes, Node.Value and Node.Children`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-forks/go-pkg-xmlx@v0.0.0-20151201012946-76f54ee73233#Document.LoadBytes>)
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
python3 parsarium.py build xml go github_com_go_forks_go_pkg_xmlx
python3 parsarium.py run xml go github_com_go_forks_go_pkg_xmlx controls/xml/catalog-ns.xml
```
