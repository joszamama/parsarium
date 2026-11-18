# xmlschema — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.3.2`
- **Upstream:** [source repository](<https://github.com/sissaschool/xmlschema>) · [PyPI](<https://pypi.org/project/xmlschema/>)
- **License:** MIT
- **Parser family:** xmlschema XMLResource namespace-tracking loader over CPython xml.etree.ElementTree.iterparse (C _elementtree XMLParser/TreeBuilder) / pyexpat / Expat 2.10.0
- **Local input API:** `xmlschema.XMLResource(BytesIO(local XML bytes)) with default options (defuse='remote', lazy=False, iterparse=xml.etree.ElementTree.iterparse); XMLResource.root (Element.tag, attrib, text and tail) and XMLResource.get_xmlns(element) for each element's own xmlns declarations`
- **Documentation:** [API reference](<https://xmlschema.readthedocs.io/en/stable/api.html#xmlschema.XMLResource>)
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
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ],
  "root": "{urn:parsarium:catalog}catalog"
}
```

## Verification scope

Shared Expat family, not an independent XML engine: xmlschema.XMLResource(BytesIO(data)) runs XMLResourceLoader._parse over CPython's default xml.etree.ElementTree.iterparse with start-ns, end-ns, start, comment, pi and end events; the pure-Python iterparse/XMLPullParser driver feeds the C _elementtree XMLParser over pyexpat and Expat 2.10.0, and the C TreeBuilder builds the tree. xmlschema adds namespace bookkeeping of its own: a namespace-map stack, each element's in-scope map (get_nsmap) and each element's own xmlns declarations (get_xmlns), plus MAX_XML_DEPTH/MAX_XML_ELEMENTS checks. The pinned image asserts the default iterparse, the C XMLParser and TreeBuilder, and pyexpat.EXPAT_VERSION; the feedback check also asserts that the BytesIO source has no URL or file object and is neither defused nor lazy. Both shared valid namespace controls match the lxml path's full summary, including the xmlns declaration count, and an independent lxml 6.1.3/libxml2 2.15.4 oracle run in the verified lxml image; xmlschema's per-element in-scope namespace maps equal lxml's nsmap on every element (including the xmlns="" undeclaration on <plain>), and the URIs of the documented get_namespaces(root_only=False) equal the declared non-empty URIs. The first control executes 110 xmlschema lines in 4 files (44 in resources/xml_loader.py, 37 in resources/xml_resource.py), 43 CPython xml/etree/ElementTree.py driver lines and 3,449 Expat lines (2,216 in xmlparse.c); the second executes 110, 51 and 3,589 (2,237). The AFL++ bridge maps the XMLResource call's Python lines, each tagged with its AFL++ hit-count bucket, plus Expat regions and branches: five identical runs of each control yield identical features, and the second control changes 611 Expat features, 14 ElementTree.py features, 20 xmlschema features and 596 AFL++ tuple IDs. xmlschema executes the same 110 lines on both controls; its differential comes from hit counts in resources/xml_loader.py: the nsmap-stack push for namespace-declaring elements (1 vs 2), start-ns appends (2 vs 3), end-ns handling and the event loop. PYTHONHASHSEED=1 is fixed because pyexpat passes CPython's hash secret to XML_SetHashSalt and a zero seed makes Expat draw a random salt. CPython's ElementTree.py, pyexpat and _elementtree are Ubuntu's distribution build; only Expat is source-built, and the C XMLParser and TreeBuilder are not covered. The harness passes BytesIO, not raw bytes: XMLResource treats a bytes source without a newline that does not start with '<' as a URL or file path. The controls do not establish DTD, entity, security, limit, non-UTF-8, XML 1.1 or malformed-input behavior; comments and processing instructions are not kept in the tree. get_xmlns, used for the declaration count, is a public method with a docstring but is not listed on the Sphinx API page. The 7,391,962 last-month PyPI downloads are package-level, mostly XSD validation and decoding use, and do not measure XMLResource parsing.

## Run this target

```sh
python3 parsarium.py build xml python xmlschema
python3 parsarium.py run xml python xmlschema controls/xml/catalog-ns.xml
```
