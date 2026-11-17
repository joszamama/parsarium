# libnxml — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.18.6`
- **License:** LGPL-2.1-or-later
- **Parser family:** nXML (Andrea Marchesini's libnxml)
- **Local input API:** `nxml_new(&doc); nxml_parse_buffer(doc, copy of the local bytes, size); walk doc->data and each nxml_data_t's children/next with type, value, ns and the attributes list (name, value, ns); nxml_free(doc)`
- **Documentation:** [API reference](<https://github.com/bakulf/libnxml/blob/0.18.6/src/nxml.h.in>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/libnxml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "xmlns:c=urn:parsarium:catalog",
    "xmlns=urn:parsarium:item",
    "version=1",
    "id=a1",
    "c:lang=es",
    "id=b2"
  ],
  "elements": [
    "c:catalog",
    "item",
    "item",
    "name",
    "note"
  ],
  "max_depth": 3,
  "root": "c:catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Verification scope

Measured as a raw-name XML tree path, not as a namespace-aware parser. Qualified element and attribute names, attribute order and xmlns declarations are compared as strings with expat in non-namespace mode. libnxml's own namespace pass is visible only as the stored prefix/local split, which the adapter re-joins; on catalog-ns.xml that pass also binds the unprefixed version and id attributes to urn:parsarium:item, so its URIs would not match Namespaces in XML and are not reported.

## Run this target

```sh
python3 parsarium.py build xml c libnxml
python3 parsarium.py run xml c libnxml controls/xml/catalog-ns.xml
```
