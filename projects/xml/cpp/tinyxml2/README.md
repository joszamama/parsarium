# TinyXML2 — XML / C++

Pinned release: `11.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, controls, parser family, and limits](../../../../catalog/xml/cpp/tinyxml2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp tinyxml2
python3 parsarium.py run xml cpp tinyxml2 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp tinyxml2 CORPUS_DIR runs/xml-tinyxml2-replay
python3 parsarium.py afl build xml cpp tinyxml2
python3 parsarium.py afl prepare xml cpp tinyxml2 runs/xml-tinyxml2-afl
python3 parsarium.py afl run runs/xml-tinyxml2-afl --check
```

TinyXML2 rejects the processing instruction in the shared `order-default-ns.xml` control. The pinned second valid control, `controls/xml/order-default-ns-no-pi.xml`, removes that instruction and otherwise has the same structure. The adapter resolves namespaces from parsed attributes; TinyXML2 itself preserves qualified names. AFL++ preparation creates a seeded run, and `--check` verifies the launch without starting a campaign.
