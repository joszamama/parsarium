# libxml2 — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.15.4`
- **Upstream:** [source repository](<https://gitlab.gnome.org/GNOME/libxml2>) · [Debian](<https://tracker.debian.org/pkg/libxml2>)
- **License:** MIT
- **Parser family:** libxml2 (GNOME libxml2, Daniel Veillard's parser)
- **Local input API:** `xmlReaderForMemory(local bytes, size, NULL, "UTF-8", XML_PARSE_NONET | XML_PARSE_NO_XXE); xmlTextReaderRead loop; xmlTextReaderNodeType, xmlTextReaderConstNamespaceUri, xmlTextReaderConstLocalName, xmlTextReaderMoveToNextAttribute, xmlTextReaderConstValue, xmlTextReaderDepth`
- **Documentation:** [API reference](<https://gnome.pages.gitlab.gnome.org/libxml2/html/xmlreader_8h.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/libxml2/verification.json)

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
python3 parsarium.py build xml c libxml2
python3 parsarium.py run xml c libxml2 controls/xml/catalog-ns.xml
```
