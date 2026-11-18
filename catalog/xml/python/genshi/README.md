# genshi — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.7.12`
- **Upstream:** [source repository](<https://github.com/edgewall/genshi>) · [PyPI](<https://pypi.org/project/genshi/>)
- **License:** BSD-3-Clause
- **Parser family:** Genshi markup-stream builder over CPython pyexpat / Expat 2.10.0 (namespace mode)
- **Local input API:** `genshi.input.XMLParser(BytesIO(bytes of a local XML file), filename) iterated to the end; the documented markup-stream events START (QName, Attrs), END, TEXT, START_NS (prefix, uri), COMMENT and PI are read through QName.namespace/localname`
- **Documentation:** [API reference](<https://genshi.edgewall.org/wiki/ApiDocs/genshi.input>)
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

Namespace-aware path over a shared parser family, not an independent XML tokenizer: genshi.input.XMLParser creates a CPython pyexpat parser in namespace mode itself and turns its callbacks into Genshi stream events, so QNames carry the URIs Expat resolved and START_NS events carry the declarations. Both valid controls match the shared namespace-aware expat oracle and the verified lxml/libxml2 path's outputs exactly, including the declaration count. The first control executes 105 Genshi lines and 3217 Expat lines. Five identical runs of each control yield identical features (4338 and 4631) and AFL++ maps (4177 and 4458 tuples); the second control changes 669 Expat features, 631 tuple IDs and 4 Genshi lines (its comment, processing-instruction and CDATA handlers in input.py), so the input-dependent feedback is mainly shared Expat feedback, labelled as for jxmlease and defusedxml. The 188,414 last-month downloads (2026-11-18) are package-level downloads of a templating toolkit.

## Run this target

```sh
python3 parsarium.py build xml python genshi
python3 parsarium.py run xml python genshi controls/xml/catalog-ns.xml
```
