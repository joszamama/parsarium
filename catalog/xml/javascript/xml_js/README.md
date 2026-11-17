# xml-js — XML / JavaScript

**Verified API path in an incomplete format cell.** The selected parser family is sax-js, shared with `sax` and `xml2js`; this package adds ordered tree construction.

- **Pinned release:** `xml-js` 1.6.11 (MIT); `sax` 1.6.1 (BlueOak-1.0.0)
- **Local input API:** [`xmljs.xml2js(text, { compact: false })`](https://github.com/nashwaan/xml-js/blob/f0376f265c4f299100fb4766828ebf066a0edeec/README.md) after strict UTF-8 decode of local bytes. `xml-js` passes the text to `sax.parser(true, {})`, then builds an ordered tree from its events.
- **Adoption:** 58,150,955 npm downloads in the saved 30-day period (2026-10-17 to 2026-11-15), seventh among the verified JavaScript XML paths at this point. Downloads include transitive use and are comparable only within this ecosystem and period.
- **Controls:** [prefixed catalog](../../../../controls/xml/catalog-ns.xml) and [default namespace order](../../../../controls/xml/order-default-ns.xml).
- **Evidence:** [parser record](../../../../data/javascript/xml/parsers.json), [source lock](../../../../projects/xml/javascript/xml_js/source-lock.json), [Docker control receipt](../../../../projects/xml/javascript/xml_js/verification.json), [AFL++ differential](../../../../data/javascript/xml/xml-js-feedback-differential.json).

The adapter returns the same ordered element names, attributes, text, namespace declarations, namespace URIs, root and maximum depth as the independent Expat oracle on both controls. `xml-js` retains comments and processing instructions in its ordered tree. The adapter expands qualified names from in-scope `xmlns` attributes; this projection is outside package-source coverage.

The Docker control covers 163 lines in `xml-js/lib/xml2js.js` and 888 lines in `sax/lib/sax.js`, separately. AFL++ feedback is scoped to the underlying `sax/lib/sax.js` source ranges; repeated replays are stable and the two valid controls differ by 40 source features and 40 bitmap tuples. The optional `node-expat` import is unused because this release hardcodes its pure JavaScript parser path. These two controls do not establish complete XML conformance. No malformed-input, resource-use, or fuzz campaign was run.

## Run

```sh
python3 parsarium.py build xml javascript xml_js
python3 parsarium.py run xml javascript xml_js controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript xml_js CORPUS_DIR runs/xml-xml-js-replay
python3 parsarium.py afl build xml javascript xml_js
python3 parsarium.py afl prepare xml javascript xml_js runs/xml-xml-js-afl
```

The AFL++ preparation command seeds a run and does not start a campaign.
