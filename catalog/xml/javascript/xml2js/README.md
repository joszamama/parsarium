# xml2js — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.6.2`
- **Upstream:** [source repository](<https://github.com/Leonidas-from-XIV/node-xml2js>) · [npm](<https://www.npmjs.com/package/xml2js>)
- **License:** MIT
- **Parser family:** sax-js strict XML state machine (sax 1.6.1) under the xml2js object builder
- **Local input API:** `new xml2js.Parser({xmlns: true, explicitChildren: true, preserveChildrenOrder: true, charsAsChildren: true, includeWhiteChars: true, charkey: '#text'}).parseStringPromise(text) on local bytes decoded with strict UTF-8 TextDecoder; xml2js runs sax.parser(strict=true, {xmlns: true}) and the adapter reads the resulting object tree: $ns element URIs and local names, sax attribute objects under $, and document-ordered element and text children under $$`
- **Documentation:** [API reference](<https://github.com/Leonidas-from-XIV/node-xml2js/blob/0.6.2/README.md>)
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

xml2js is an API path over the selected sax 1.6.1 tokenizer, not a separate parser engine; the receipt counts xml2js package lines and sax lib/sax.js lines separately, and AFL++ feedback spans both. Both valid controls, catalog-ns.xml and order-default-ns.xml, match the expat oracle exactly, including namespace URIs, attribute order and text. Scope limits: xml2js drops comment and processing-instruction events, so a text run split only by a comment or PI is reported as one segment where expat reports two (both controls place them beside whitespace only); xml2js does not pass sax strictEntities, so sax's HTML-extended entity table is accepted; DOCTYPE events are ignored. The adapter sets the documented charkey option to '#text' because the default '_' is a legal element name. No malformed-input, resource-use, or fuzz campaign was run.

## Run this target

```sh
python3 parsarium.py build xml javascript xml2js
python3 parsarium.py run xml javascript xml2js controls/xml/catalog-ns.xml
```
