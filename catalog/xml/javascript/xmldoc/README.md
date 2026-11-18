# xmldoc — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.0.0`
- **Upstream:** [source repository](<https://github.com/nfarina/xmldoc>) · [npm](<https://www.npmjs.com/package/xmldoc>)
- **License:** MIT
- **Parser family:** sax-js strict XML state machine (sax 1.6.1 in non-namespace mode), shared with the selected sax path, xml2js and xml-js
- **Local input API:** `new XmlDocument(xml: string) (ESM import { XmlDocument } from 'xmldoc'), after strict UTF-8 TextDecoder of local bytes; the result is read through the documented members name, attr and children (type element, text, cdata, comment) and doctype`
- **Documentation:** [API reference](<https://github.com/nfarina/xmldoc/blob/3a5eb7c0af49006b7eede95114c7be49adfde61d/README.md>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/javascript/xml/parsers.json) · [control result](../../../../data/javascript/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "xmlns:c=urn:parsarium:catalog",
    "xmlns=urn:parsarium:item",
    "version=1",
    "id=a1",
    "c:lang=es",
    "id=b2"
  ],
  "cdata_sections": 1,
  "comments": [],
  "doctype": "",
  "elements": [
    "c:catalog",
    "item",
    "item",
    "name",
    "note"
  ],
  "max_depth": 3,
  "root": "c:catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Verification scope

Measured as a raw-name XML tree path, not as a namespace-aware XML parser. xmldoc documents that namespaces are ignored (<office:body> becomes "office:body"), so prefixes, local names, attribute order and xmlns declarations are compared as raw qualified-name strings; no namespace URI, expanded name or in-scope binding is produced by xmldoc or inferred by the harness. The comparison oracle is expat in non-namespace mode restricted to what the tree keeps. Fields xmldoc exposes but the oracle cannot (line, column, position, startTagPosition, val) are not compared.

## Run this target

```sh
python3 parsarium.py build xml javascript xmldoc
python3 parsarium.py run xml javascript xmldoc controls/xml/catalog-ns.xml
```
