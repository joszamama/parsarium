# expat — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.10.0`
- **Upstream:** [source repository](<https://github.com/libexpat/libexpat>) · [Debian](<https://tracker.debian.org/pkg/expat>)
- **License:** MIT
- **Parser family:** expat (James Clark's expat, maintained as libexpat)
- **Local input API:** `XML_ParserCreateNS("UTF-8", ' '); XML_SetHashSalt(parser, fixed non-zero salt); element, namespace-declaration, character-data, comment and processing-instruction handlers; XML_Parse(parser, local bytes, size, XML_TRUE)`
- **Documentation:** [API reference](<https://libexpat.github.io/doc/api/latest/>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/expat/verification.json)

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
python3 parsarium.py build xml c expat
python3 parsarium.py run xml c expat controls/xml/catalog-ns.xml
```
