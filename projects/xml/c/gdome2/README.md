# gdome2 — XML / C

Pinned release: `0.8.1+debian-10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/gdome2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c gdome2
python3 parsarium.py run xml c gdome2 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c gdome2 CORPUS_DIR runs/xml-gdome2-replay
python3 parsarium.py afl build xml c gdome2
python3 parsarium.py afl prepare xml c gdome2 runs/xml-gdome2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish gdome2's namespace-aware DOM Level 2 view (element and attribute namespaceURI/localName, namespace declarations exposed as attributes in the xmlns namespace, attribute order and decoded values, depth, text and CDATA nodes) for them only. gdome2 builds its DOM over libxml2's tree (xmlParseMemory), so this is a libxml2-family path: the input-dependent feedback comes mostly from libxml2, with gdome2's own node, element and attribute-map lines also differing between the controls. Comments and processing instructions are DOM nodes but are not reported; the order control's sit in whitespace-only runs. DTDs, entities beyond the controls' references, other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from controls/xml/check_controls.py (Python pyexpat, a different family).
