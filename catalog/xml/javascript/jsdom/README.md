# jsdom — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `31.0.1`
- **License:** MIT
- **Parser family:** saxes XML 1.0 + Namespaces state machine (saxes 6.0.0) under jsdom's XML document builder
- **Local input API:** `new JSDOM(text, {contentType: 'application/xml', virtualConsole}) on local bytes decoded with strict UTF-8 TextDecoder; jsdom's XML document parser runs new SaxesParser({xmlns: true, defaultXMLVersion: '1.0', forceXMLVersion: true}), throws a SyntaxError on the first saxes error, and builds the DOM; the adapter treats any jsdomError as fatal and reads window.document: element and attribute namespaceURI/localName, attribute order, and Text/CDATASection data in document order`
- **Documentation:** [API reference](<https://github.com/jsdom/jsdom/blob/31.0.1/README.md>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/javascript/xml/parsers.json) · [control result](../../../../data/javascript/xml/verification.json)

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

jsdom is an API path over the selected saxes 6.0.0 tokenizer, not a separate parser engine; the receipt counts jsdom package lines, jsdom's own XML document parser lib/jsdom/browser/parser/xml.js alone, and saxes saxes.js lines separately. The jsdom package count is dominated by module loading and window setup; the coverage run only constructs the document and closes the window, so the adapter's DOM read-back is not counted. Both valid controls, catalog-ns.xml and order-default-ns.xml, match the expat oracle exactly, including namespace URIs, attribute order and text; comments and processing instructions remain DOM nodes and split text as in expat. AFL++ feedback spans /work/node_modules/ during construction only: saxes, jsdom XML tree construction and DOM node creation, plus input-independent module-load and window setup ranges; window named-property and id-cache updates from id attributes are input-dependent jsdom construction, and xmlchars ranges are saxes character-class checks. Scope limits: jsdom copies DOCTYPE <!ENTITY name "value"> declarations into saxes' entity table (a jsdom extension, not general DTD processing), forces XML 1.0 rules for version 1.1 documents, and drops text outside the root element. DOMParser.parseFromString shares parseIntoDocument but turns errors into a parsererror document; it was not the measured path. No malformed-input, resource-use, or fuzz campaign was run.

## Run this target

```sh
python3 parsarium.py build xml javascript jsdom
python3 parsarium.py run xml javascript jsdom controls/xml/catalog-ns.xml
```
