# htmlparser2 — XML / JavaScript (candidate)

Pinned release: `12.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json) · [candidate row](../../../../data/javascript/xml/htmlparser2-candidate.json) · [feedback receipt](../../../../data/javascript/xml/htmlparser2-feedback-differential.json)

Measured path: `new Parser(handler, {xmlMode: true}).write(text)` then `end()`. htmlparser2 does not resolve namespaces or check well-formedness, so outputs are raw qualified names and `xmlns` declarations stay ordinary attributes. [oracle.py](oracle.py) runs expat without namespace processing over the same fields.

## Run from the repository root

```sh
python3 parsarium.py build xml javascript htmlparser2
python3 parsarium.py run xml javascript htmlparser2 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript htmlparser2 CORPUS_DIR runs/xml-htmlparser2-replay
python3 parsarium.py afl build xml javascript htmlparser2
python3 parsarium.py afl prepare xml javascript htmlparser2 runs/xml-htmlparser2-afl
python3 scripts/verify_javascript_xml_htmlparser2.py --check
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
