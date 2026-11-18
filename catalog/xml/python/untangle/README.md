# untangle — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.3.1`
- **Upstream:** [PyPI](<https://pypi.org/project/untangle/>)
- **License:** MIT
- **Parser family:** untangle SAX handler over defusedxml DefusedExpatParser over CPython xml.sax/pyexpat over Expat 2.10.0
- **Local input API:** `untangle.parse(pathlib.Path(local XML file)); Element._name, _attributes, cdata and children filled by untangle.Handler from SAX startElement/characters/endElement events`
- **Documentation:** [API reference](<https://untangle.readthedocs.io/en/latest/>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/python/xml/parsers.json) · [control result](../../../../data/python/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "version=1",
    "id=a1",
    "c:lang=es",
    "id=b2"
  ],
  "elements": [
    "c_catalog",
    "item",
    "item",
    "name",
    "note"
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
  "root": "c_catalog"
}
```

## Verification scope

Shared Expat family, not an independent XML tokenizer: untangle.parse() uses defusedxml.sax.make_parser() (DefusedExpatParser, a guarded subclass of CPython's xml.sax.expatreader.ExpatParser) over pyexpat and Expat 2.10.0, and untangle.Handler builds Element objects from startElement/characters/endElement. The pinned image asserts the parser class and pyexpat.EXPAT_VERSION. Namespace processing is off, so untangle drops namespace URIs: element names are qualified names with ':' replaced by '_' (c:catalog -> c_catalog, p:amount -> p_amount), attribute names keep their raw prefix (c:lang), and xmlns declarations remain ordinary attributes. Passing feature_namespaces=True yields an empty tree because the handler has no startElementNS. The adapter does not reconstruct URIs from the lossy names. Both shared valid namespace controls match an independent namespace-aware lxml 6.1.3/libxml2 2.15.4 oracle, run in the verified lxml image, whose expanded summary equals the lxml path's and whose projection to untangle's documented naming rule equals untangle's summary on every field; the oracle records which expanded names untangle loses. The first control executes 49 untangle/defusedxml lines (35 in untangle/__init__.py), 111 CPython xml/sax driver lines and 2,238 Expat lines (1,509 in xmlparse.c); the second executes 49, 112 and 2,475 (1,586). The AFL++ bridge maps the untangle.parse call's untangle/defusedxml/xml.sax lines plus Expat regions and branches: five identical runs of each control yield identical features, and the second control changes 829 Expat features, 1 SAX-driver line and 792 AFL++ tuple IDs; untangle's own 49 package lines are identical on both controls, so input dependence on these controls comes from Expat and the SAX dispatch. PYTHONHASHSEED=1 is fixed because pyexpat passes CPython's hash secret to XML_SetHashSalt and a zero seed makes Expat draw a random salt. The controls do not establish DTD, entity, non-UTF-8, XML 1.1 or malformed-input behavior. Comments and processing instructions are not kept, and mixed-content text is concatenated per element. The 310,666 last-month PyPI downloads are package-level and do not measure XML parsing.

## Run this target

```sh
python3 parsarium.py build xml python untangle
python3 parsarium.py run xml python untangle controls/xml/catalog-ns.xml
```
