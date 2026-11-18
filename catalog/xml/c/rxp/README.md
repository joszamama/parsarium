# rxp — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.5.0`
- **License:** GPL-2.0
- **Parser family:** RXP (Edinburgh LTG)
- **Local input API:** `init_parser(); NewParser(); ParserSetFlag(p, XMLNamespaces, 1); ParserSetFlag(p, ReturnComments, 1); ParserSetWarningCallback; NewExternalEntity(0, 0, local file, 0, 0); EntityOpen; ParserPush; ReadXBit until XBIT_eof (XBIT_start/empty: element_definition, ns_element_definition, attributes with definition/ns_definition/value; XBIT_end; XBIT_pcdata; XBIT_cdsect; XBIT_comment; XBIT_pi); FreeXBit; FreeDtd; FreeParser; FreeEntity`
- **Documentation:** [API reference](<https://sources.debian.org/src/rxp/1.5.0-3.1/doc/Manual/>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/rxp/verification.json)

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

Namespace-aware path without a declaration count: RXP returns no xmlns declarations and documents no binding list, so the shared expected outputs are compared with namespace_declarations dropped (as for Python's defusedxml). Unprefixed attributes, which RXP files as per-element-type attributes under the element's namespace, are reported with no namespace.

## Run this target

```sh
python3 parsarium.py build xml c rxp
python3 parsarium.py run xml c rxp controls/xml/catalog-ns.xml
```
