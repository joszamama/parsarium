# mxml — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.0.6`
- **License:** Apache-2.0
- **Parser family:** Mini-XML (Michael R Sweet's mxml)
- **Local input API:** `mxmlOptionsNew(); mxmlOptionsSetTypeValue(options, MXML_TYPE_OPAQUE); mxmlOptionsSetErrorCallback; mxmlLoadString(NULL, options, NUL-terminated copy of the local bytes); tree walk with mxmlGetType, mxmlGetFirstChild, mxmlGetNextSibling, mxmlGetParent, mxmlGetElement, mxmlElementGetAttrCount, mxmlElementGetAttrByIndex, mxmlGetOpaque, mxmlGetCDATA. Namespace resolution is done by the adapter, not by mxml`
- **Documentation:** [API reference](<https://www.msweet.org/mxml/mxml.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/mxml/verification.json)

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
python3 parsarium.py build xml c mxml
python3 parsarium.py run xml c mxml controls/xml/catalog-ns.xml
```
