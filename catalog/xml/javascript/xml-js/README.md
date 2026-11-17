# xml-js — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.6.11`
- **License:** MIT
- **Parser family:** sax-js strict XML state machine (sax 1.6.1) under xml-js tree builder
- **Local input API:** `xmljs.xml2js(text, {compact:false, captureSpacesBetweenElements:true, alwaysChildren:true}) on strictly UTF-8 decoded local bytes; ordered tree builder over strict sax.parser(true) events`
- **Documentation:** [API reference](<https://github.com/nashwaan/xml-js/blob/f0376f265c4f299100fb4766828ebf066a0edeec/README.md>)
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

Docker valid-control replay matches the Expat oracle on both namespace-aware controls. V8 coverage counts 163 xml-js lib/xml2js.js tree-builder lines and 888 underlying sax lib/sax.js tokenizer lines separately. AFL++ feedback is scoped to the sax file only and is stable on repeated valid-control replays with an input-dependent 40-feature/40-tuple difference. xml-js delegates tokenization to the same sax 1.6.1 code selected independently as sax and by xml2js; it adds ordered tree construction, not an independent tokenizer. Namespace URI expansion is done by the adapter from preserved xmlns attributes. The hardcoded pureJsParser=true path does not use the optional node-expat import. Two valid controls do not prove complete XML conformance; no malformed, resource-use or campaign tests were run.

## Run this target

```sh
python3 parsarium.py build xml javascript xml_js
python3 parsarium.py run xml javascript xml_js controls/xml/catalog-ns.xml
```
