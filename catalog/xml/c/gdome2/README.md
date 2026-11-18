# gdome2 — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.8.1+debian-10`
- **Upstream:** [Debian](<https://tracker.debian.org/pkg/gdome2>)
- **License:** LGPL-2.1-or-later
- **Parser family:** libxml2 (via gdome2's DOM Level 2 layer)
- **Local input API:** `gdome_di_mkref(); gdome_di_createDocFromMemory(impl, NUL-terminated copy of the local bytes, GDOME_LOAD_PARSING, &exc); walk from gdome_doc_documentElement with gdome_n_nodeType, gdome_n_namespaceURI, gdome_n_localName, gdome_n_nodeName, gdome_n_nodeValue, gdome_n_attributes/gdome_nnm_length/gdome_nnm_item, gdome_n_firstChild and gdome_n_nextSibling; gdome_doc_unref, gdome_di_unref`
- **Documentation:** [API reference](<https://sources.debian.org/src/gdome2/0.8.1%2Bdebian-10/gtk-doc/html/gdome2-gdomedomimplementation.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/gdome2/verification.json)

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

Namespace-aware path: both valid controls give the exact shared summary, including the declaration count, from gdome2's own namespaceURI/localName accessors and its xmlns-namespace declaration attributes.

## Run this target

```sh
python3 parsarium.py build xml c gdome2
python3 parsarium.py run xml c gdome2 controls/xml/catalog-ns.xml
```
