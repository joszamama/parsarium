# defusedxml — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.7.1`
- **License:** PSF-2.0
- **Parser family:** defusedxml guarded ElementTree facade over CPython xml.etree.ElementTree XMLParser/pyexpat over Expat 2.10.0
- **Local input API:** `defusedxml.ElementTree.parse(BytesIO(local XML bytes)) with default forbid_dtd=False, forbid_entities=True, forbid_external=True; getroot(); Element.tag, attrib, text and tail`
- **Documentation:** [API reference](<https://github.com/tiran/defusedxml/blob/v0.7.1/README.md>)
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
  "namespaces": [
    "urn:parsarium:catalog",
    "urn:parsarium:item"
  ],
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ],
  "root": "{urn:parsarium:catalog}catalog"
}
```

## Verification scope

Shared Expat family, not an independent XML engine: defusedxml.ElementTree.parse() builds DefusedXMLParser, a subclass of CPython's pure-Python xml.etree.ElementTree.XMLParser (defusedxml re-imports ElementTree.py with the _elementtree accelerator blocked), whose own additions are guard handlers installed on pyexpat for entity declarations, unparsed entity declarations and external entity references; stdlib ElementTree.parse feeds the stream, Expat 2.10.0 tokenizes and checks well-formedness, ElementTree.py's XMLParser callbacks expand namespace names, and the C _elementtree TreeBuilder builds the tree. The pinned image asserts the pure-Python base class, the C TreeBuilder target, the installed guards and pyexpat.EXPAT_VERSION. ElementTree resolves namespaces ({uri}local tags and attribute names) but keeps no xmlns declarations or prefixes, so the summary omits the lxml path's namespace_declarations count and lists the URIs carried by expanded names. Both shared valid namespace controls match an independent namespace-aware lxml 6.1.3/libxml2 2.15.4 oracle, run in the verified lxml image, on every remaining field; the oracle's summary equals the lxml path's without the declaration count, and its expanded-name URIs equal its declared non-empty URIs on both controls. The first control executes 20 defusedxml lines (13 in defusedxml/ElementTree.py, 7 in common.py), 71 CPython xml/etree/ElementTree.py driver lines and 2,560 Expat lines (1,808 in xmlparse.c); the second executes 20, 79 and 2,806 (1,894). The AFL++ bridge maps the parse call's defusedxml/ElementTree.py lines plus Expat regions and branches: five identical runs of each control yield identical features, and the second control changes 840 Expat features, 8 ElementTree.py lines and 800 AFL++ tuple IDs. defusedxml's own 20 lines (guard installation and the parse factory) are identical on both controls; they are kept as features because the guard callbacks would run only on DTD entity or external-reference input, which was not tested. Input dependence on these controls comes from Expat and the ElementTree driver. PYTHONHASHSEED=1 is fixed because pyexpat passes CPython's hash secret to XML_SetHashSalt and a zero seed makes Expat draw a random salt. CPython's ElementTree.py, pyexpat and _elementtree are Ubuntu's distribution build; only Expat is source-built, and the C TreeBuilder is not covered. The controls do not establish DTD, entity, security, non-UTF-8, XML 1.1 or malformed-input behavior; comments and processing instructions are dropped by the default TreeBuilder. The 270,848,271 last-month PyPI downloads are package-level, largely transitive, and do not measure XML parsing.

## Run this target

```sh
python3 parsarium.py build xml python defusedxml
python3 parsarium.py run xml python defusedxml controls/xml/catalog-ns.xml
```
