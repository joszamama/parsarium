# pyquery — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.1.0`
- **Upstream:** [source repository](<https://github.com/gawel/pyquery>) · [PyPI](<https://pypi.org/project/pyquery/>)
- **License:** BSD-3-Clause
- **Parser family:** pyquery PyQuery over lxml.etree.fromstring (default XMLParser) over libxml2 2.15.4 XML parser
- **Local input API:** `pyquery.PyQuery(local XML bytes, parser="xml"); PyQuery.contents() recursion (child text nodes and child elements) over the returned lxml elements' tag, attrib and nsmap`
- **Documentation:** [API reference](<https://pyquery.readthedocs.io/en/latest/tips.html#using-different-parsers>)
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

Shared parser family, not an independent XML tokenizer: PyQuery(bytes, parser='xml') hands the bytes to lxml.etree.fromstring with lxml's default XMLParser, and libxml2 tokenizes them; pyquery wraps the returned lxml elements in its jQuery-style list. The pinned image installs pyquery 2.1.0 with lxml 6.1.3 linked to source-built libxml2 2.15.4 and asserts the parser='xml' route. Both valid namespace controls match their expected summaries, and an independent CPython pyexpat oracle in namespace mode gives the same values for the keys pyquery reports (comments and processing instructions are not returned by contents()). The first control executes 48 pyquery/pyquery.py lines and 1,475 libxml2 parser.c lines. The AFL++ bridge maps executed pyquery lines plus parser.c regions: five identical runs of each control yield identical features (884 and 983) and AFL++ maps (876 and 973 tuples); the second control changes 213 parser.c features, 209 tuple IDs and no pyquery line, so all input-dependent feedback comes from libxml2 (the Parsel wrapper precedent, labelled as shared-parser feedback). parser.c lines 8700-8720 are excluded as in the lxml path. The 1,326,240 last-month downloads are package-level and mostly HTML scraping use.

## Run this target

```sh
python3 parsarium.py build xml python pyquery
python3 parsarium.py run xml python pyquery controls/xml/catalog-ns.xml
```
