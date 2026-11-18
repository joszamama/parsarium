# @xml-tools/parser — XML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.12`
- **Upstream:** [source repository](<https://github.com/SAP/app-studio-toolkit>) · [npm](<https://www.npmjs.com/package/@xml-tools/parser>)
- **License:** Apache-2.0
- **Parser family:** @xml-tools/parser XML lexer and grammar over Chevrotain 7.1.1 CST engine
- **Local input API:** `parse(text) on strictly UTF-8 decoded local bytes; returns Chevrotain XML CST, token vector, lexErrors and parseErrors`
- **Documentation:** [API reference](<https://unpkg.com/@xml-tools/parser@1.0.12/README.md>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/javascript/xml/parsers.json) · [control result](../../../../data/javascript/xml/verification.json)

## Observed control result

```json
{
  "tree": {
    "qname": "c:catalog",
    "attributes": [
      {
        "qname": "xmlns:c",
        "raw_value": "\"urn:parsarium:catalog\""
      },
      {
        "qname": "xmlns",
        "raw_value": "\"urn:parsarium:item\""
      },
      {
        "qname": "version",
        "raw_value": "\"1\""
      }
    ],
    "children": [
      {
        "qname": "item",
        "attributes": [
          {
            "qname": "id",
            "raw_value": "\"a1\""
          },
          {
            "qname": "c:lang",
            "raw_value": "\"es\""
          }
        ],
        "children": []
      },
      {
        "qname": "item",
        "attributes": [
          {
            "qname": "id",
            "raw_value": "\"b2\""
          }
        ],
        "children": [
          {
            "qname": "name",
            "attributes": [],
            "children": []
          },
          {
            "qname": "note",
            "attributes": [],
            "children": []
          }
        ]
      }
    ]
  },
  "max_depth": 3,
  "token_count": 70,
  "lex_errors": 0,
  "parse_errors": 0
}
```

## Verification scope

Docker control and fixed second valid control return exact hierarchical raw-QName CST projections with zero lex/parse errors; Expat without namespace expansion independently confirms name hierarchy. V8 coverage reports 351 package grammar/lexer lines and 5,225 Chevrotain engine lines separately. AFL++ hit-count guidance is confined to package parser.js ALT callbacks; three repeats per control are stable, with 22 feature and 22 tuple differences across 11 changed parser hit counts. Read/decode-only baselines match across both controls and show 17 constructor self-analysis features. No expanded namespace URI, decoded entity text, new branch/line, malformed-input, or campaign claim. Selected as a limited raw-QName XML CST parser; output and feedback are confined to the documented projection.

## Run this target

```sh
python3 parsarium.py build xml javascript xml_tools_parser
python3 parsarium.py run xml javascript xml_tools_parser controls/xml/catalog-ns.xml
```
