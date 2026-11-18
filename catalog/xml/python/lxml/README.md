# lxml — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `6.1.3`
- **Upstream:** [source repository](<https://github.com/lxml/lxml>) · [PyPI](<https://pypi.org/project/lxml/>)
- **License:** BSD-3-Clause
- **Parser family:** lxml.etree binding over libxml2 2.15.4 XML parser
- **Local input API:** `lxml.etree.parse(BytesIO(local XML bytes), XMLParser(resolve_entities=False, no_network=True, recover=False)).getroot(); Element.tag, attrib, nsmap, text and tail`
- **Documentation:** [API reference](<https://lxml.de/parsing.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/python/xml/parsers.json) · [control result](../../../../data/python/xml/verification.json)

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

## Verification scope

The pinned image links lxml.etree to source-built libxml2 2.15.4. Its first valid namespace control covers 1,463 lines in libxml2 parser.c; the second valid control matches its exact expected tree. The AFL++ bridge maps executed parser.c lines, with five identical control runs yielding identical feedback and the second control changing 213 parser lines and 209 AFL++ tuple IDs. Lines 8700–8720 of parser.c are excluded from AFL++ feedback because an address-sensitive attribute lookup varied across identical replays; they remain in the source coverage report. The two controls do not establish DTD, external entity, non-UTF-8, or XML 1.1 behavior.

## Run this target

```sh
python3 parsarium.py build xml python lxml
python3 parsarium.py run xml python lxml controls/xml/catalog-ns.xml
```
