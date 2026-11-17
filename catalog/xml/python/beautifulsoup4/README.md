# beautifulsoup4 — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.15.0`
- **License:** MIT
- **Parser family:** Beautiful Soup bs4 tree builder over lxml.etree XMLParser over libxml2 2.15.4 XML parser
- **Local input API:** `bs4.BeautifulSoup(local XML bytes, "xml"); Tag.namespace, Tag.name, NamespacedAttribute.namespace/name, NavigableString, Comment and XMLProcessingInstruction children of the resulting bs4 tree`
- **Documentation:** [API reference](<https://www.crummy.com/software/BeautifulSoup/bs4/doc/#parsing-xml>)
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

Shared parser family, not an independent XML tokenizer: Beautiful Soup's documented "xml" builder (the docs call lxml "the only currently supported XML parser") feeds the bytes to lxml.etree.XMLParser(target=builder, recover=True), and libxml2 tokenizes them; bs4 builds its own tree from lxml's callbacks. The pinned image installs bs4 4.15.0 with lxml 6.1.3 linked to source-built libxml2 2.15.4 and asserts that BeautifulSoup(..., 'xml') selects LXMLTreeBuilderForXML over lxml.etree.XMLParser. Both valid namespace controls match their expected bs4-tree summaries; the element, attribute, namespace, text, depth and root fields equal the lxml path's outputs. The first control executes 450 bs4 lines in 5 files (115 in builder/_lxml.py) and 1,570 libxml2 parser.c lines. The AFL++ bridge maps executed bs4 lines plus parser.c lines: five identical runs of each control yield identical features, and the second control changes 11 bs4 lines, 236 parser.c lines and 242 AFL++ tuple IDs. parser.c lines 8700-8720 are excluded from AFL++ feedback as in the lxml path. The controls do not establish DTD, external entity, non-UTF-8, XML 1.1, or malformed-input (recover=True) behavior. The bs4 tree drops CDATA section boundaries and the XML declaration node and lists xmlns declarations after ordinary attributes. The 315,320,831 last-month PyPI downloads are package-level and mostly HTML use; they do not measure XML parsing.
