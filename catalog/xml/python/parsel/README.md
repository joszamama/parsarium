# parsel — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.12.1`
- **Upstream:** [source repository](<https://github.com/scrapy/parsel>) · [PyPI](<https://pypi.org/project/parsel/>)
- **License:** BSD-3-Clause
- **Parser family:** Parsel Selector over lxml.etree XMLParser (SafeXMLParser) over libxml2 2.15.4 XML parser
- **Local input API:** `parsel.Selector(body=local XML bytes, type="xml"); Selector.xpath() with get()/getall() for namespace-uri(), local-name(), namespace::*, ancestor-or-self::*, //text(), //comment() and //processing-instruction(), plus Selector.attrib for attributes`
- **Documentation:** [API reference](<https://parsel.readthedocs.io/en/v1.12.1/parsel.html>)
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
  "comments": [],
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
  "processing_instructions": [],
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ],
  "root": "{urn:parsarium:catalog}catalog"
}
```

## Verification scope

Shared parser family, not an independent XML tokenizer: Parsel's documented Selector(body=bytes, type='xml') hands the stripped bytes to lxml.etree.fromstring with SafeXMLParser(recover=True, resolve_entities=False, huge_tree=True), and libxml2 tokenizes them; Parsel wraps the resulting lxml tree for XPath queries. The pinned image installs parsel 1.12.1 with lxml 6.1.3 linked to source-built libxml2 2.15.4 and asserts that the 'xml' type uses parsel.selector.SafeXMLParser, an lxml.etree.XMLParser subclass. The summary is read only through Selector.xpath()/get() and Selector.attrib. Both valid namespace controls match their expected summaries, which equal the beautifulsoup4 path's, and an independent CPython pyexpat (Expat 2.7.4) oracle in namespace mode produces the same summary for both. The first control executes 100 parsel/selector.py lines and 1,484 libxml2 parser.c lines (1,484-1,493 over three replays; the order control 1,639-1,645, varying only in the address-sensitive range excluded below). The AFL++ bridge maps executed Parsel lines plus parser.c regions: five identical runs of each control yield identical features (940 and 1,039) and AFL++ maps (934 and 1,031 tuples); the second control changes 213 parser.c features and 209 tuple IDs and no Parsel line, so all input-dependent feedback comes from libxml2. parser.c lines 8700-8720 are excluded as in the lxml path. The controls do not establish DTD, external entity, non-UTF-8, XML 1.1, huge-tree or malformed-input (recover=True) behavior. CDATA boundaries and the XML declaration are not kept, and namespace declarations are counted as in-scope changes, so a redundant redeclaration would be missed. The 3,699,459 last-month PyPI downloads are package-level and mostly Scrapy HTML use; they do not measure XML parsing.

## Run this target

```sh
python3 parsarium.py build xml python parsel
python3 parsarium.py run xml python parsel controls/xml/catalog-ns.xml
```
