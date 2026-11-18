# jxmlease — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.3`
- **Upstream:** [source repository](<https://github.com/Juniper/jxmlease>) · [PyPI](<https://pypi.org/project/jxmlease/>)
- **License:** MIT
- **Parser family:** jxmlease node builder over CPython pyexpat / Expat 2.10.0 (raw names, namespace processing off)
- **Local input API:** `jxmlease.parse(bytes of a local XML file) with default settings; returned XMLDictNode / XMLListNode / XMLCDATANode tree read through tag, get_xml_attrs() and get_cdata()`
- **Documentation:** [API reference](<https://jxmlease.readthedocs.io/en/stable/parsing.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/python/xml/parsers.json) · [control result](../../../../data/python/xml/verification.json)

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
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ],
  "root": "c:catalog"
}
```

## Verification scope

Raw-name view over a shared parser family, not an independent XML tokenizer: jxmlease.parse creates a CPython pyexpat parser itself with namespace processing off and builds its node tree in _DictSAXHandler, so names are reported as written (c:catalog, c:lang, p:amount) and xmlns declarations are ordinary attributes; no namespace URI is resolved and no expanded name is claimed. Both valid controls match the expat non-namespace raw-name oracle used for the C raw-name paths exactly and an independent lxml/libxml2 parse projected to raw names (attribute multiset). The first control executes 239 jxmlease lines and 2,197 Expat source lines. The AFL++ bridge maps executed jxmlease lines plus Expat regions and branches: five identical runs of each control yield identical features (3149 and 3467) and AFL++ maps (3064 and 3373 tuples); the second control changes 794 Expat features, 757 tuple IDs and no jxmlease line, so all input-dependent feedback comes from Expat (shared-parser feedback, labelled as for defusedxml and Parsel). Same-name siblings are grouped into lists, so order across differently named siblings is not kept (both controls keep it). The 118,785 last-month downloads are package-level.

## Run this target

```sh
python3 parsarium.py build xml python jxmlease
python3 parsarium.py run xml python jxmlease controls/xml/catalog-ns.xml
```
