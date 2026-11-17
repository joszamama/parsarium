# parsel — XML / Python

Pinned release: `1.12.1`. [Manifest](manifest.json) · [verification receipt](verification.json) · [scoped catalog row](../../../../data/python/xml/parsel-parser.json) · [feedback check](../../../../data/python/xml/parsel-valid-feedback.json)

**Scoped candidate.** The catalog row lives in `data/python/xml/parsel-parser.json` until it is merged into the shared Python XML cell.

`Selector(body=bytes, type="xml")` is not an independent XML parser. Parsel strips the body, removes NUL bytes and calls `lxml.etree.fromstring` with `SafeXMLParser(recover=True, resolve_entities=False, huge_tree=True)`. libxml2 2.15.4 does the parsing, the same lxml/libxml2 family as the `lxml` and `beautifulsoup4` paths. The harness reads the tree only through `Selector.xpath()`, `get()` and `Selector.attrib`. [`oracle.py`](oracle.py) recomputes the same summary with CPython's pyexpat (Expat), and both valid controls match it.

Limits: CDATA boundaries and the XML declaration are not kept. Namespace declarations are counted as in-scope changes, so a redundant redeclaration is missed. On the two valid controls Parsel runs the same 100 lines, so all input-dependent AFL++ feedback comes from libxml2 `parser.c`. Malformed, DTD, non-UTF-8 and huge-tree input were not tested.

## Run from the repository root

```sh
python3 parsarium.py build xml python parsel
python3 parsarium.py run xml python parsel controls/xml/catalog-ns.xml
python3 parsarium.py replay xml python parsel CORPUS_DIR runs/xml-parsel-replay
python3 parsarium.py afl build xml python parsel
python3 parsarium.py afl prepare xml python parsel runs/xml-parsel-afl
python3 scripts/verify_python_xml_parsel_feedback.py
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
