# ixml — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `22.2.1`
- **Upstream:** [source repository](<https://github.com/pupnp/pupnp>)
- **License:** BSD-3-Clause
- **Parser family:** IXML (Intel/pupnp DOM parser)
- **Local input API:** `ixmlParseBufferEx(NUL-terminated copy of the local bytes, &doc); walk the DOM from ixmlNode_getFirstChild(doc) with ixmlNode_getNodeType, ixmlNode_getNodeName, ixmlNode_getNodeValue, ixmlNode_getAttributes/ixmlNamedNodeMap_item, ixmlNode_getFirstChild and ixmlNode_getNextSibling; ixmlDocument_free(doc)`
- **Documentation:** [API reference](<https://github.com/pupnp/pupnp/blob/release-22.2.1/ixml/inc/ixml.h>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/ixml/verification.json)

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

Measured as a raw-name XML tree path, not as a namespace-aware parser. Qualified element and attribute names, attribute order and xmlns declarations are compared as strings with expat in non-namespace mode. IXML's own namespaceURI fields are not used: on catalog-ns.xml the unprefixed item, name and note elements get no URI although xmlns="urn:parsarium:item" is in scope, and on order-default-ns.xml plain keeps urn:parsarium:order despite xmlns="".

## Run this target

```sh
python3 parsarium.py build xml c ixml
python3 parsarium.py run xml c ixml controls/xml/catalog-ns.xml
```
