# htmlparser2 — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `12.0.0`
- **License:** MIT
- **Parser family:** htmlparser2 forgiving HTML/XML tokenizer (own Tokenizer.js state machine) with entities decode trees
- **Local input API:** `new Parser(handler, {xmlMode: true}).write(string) then end(), after strict UTF-8 TextDecoder of local bytes; handler callbacks onopentagname, onattribute, onclosetag, ontext, oncdatastart, oncomment/oncommentend, onprocessinginstruction, onerror`
- **Documentation:** [API reference](<https://github.com/fb55/htmlparser2/blob/c73fec0c0586647cd1269d2598e2ba4203d0207f/README.md>)
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
  "elements": [
    "c:catalog",
    "item",
    "item",
    "name",
    "note"
  ],
  "max_depth": 3,
  "processing_instructions": [
    "xml version=\"1.0\" encoding=\"UTF-8\""
  ],
  "root": "c:catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Verification scope

Measured as a raw-name XML event path, not as a namespace-aware XML parser. htmlparser2 returns qualified names only, so prefixes, local names, attribute order and xmlns declarations are compared as raw qualified-name strings; no namespace URI, expanded name or in-scope binding is produced by the parser or inferred by the harness. The comparison oracle is expat in non-namespace mode, which exposes the same fields. Fields htmlparser2 exposes but the oracle cannot (attribute quote style, startIndex/endIndex) are not compared.

## Run this target

```sh
python3 parsarium.py build xml javascript htmlparser2
python3 parsarium.py run xml javascript htmlparser2 controls/xml/catalog-ns.xml
```
