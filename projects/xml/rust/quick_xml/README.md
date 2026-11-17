# quick-xml — XML / Rust

Pinned release: `0.42.0`. [Manifest](manifest.json) · [verification receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/xml/rust/quick_xml/verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/quick-xml/README.md)

The harness (`src/lib.rs`) reads an XML document from an in-memory byte slice with quick-xml's namespace-aware reader. It reports the expanded element and attribute names, the namespace declarations, and the decoded text, including character references and CDATA.

## Run from the repository root

```sh
python3 parsarium.py build xml rust quick_xml
python3 parsarium.py run xml rust quick_xml controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml rust quick_xml
python3 parsarium.py afl prepare xml rust quick_xml runs/xml-quick_xml-afl --seed controls/xml/order-default-ns.xml
python3 parsarium.py afl run runs/xml-quick_xml-afl --check
```

`afl build` builds the afl.rs overlay. It then runs `afl-showmap` three times on each of the two fixed valid controls and records the edge counts and their stability. The AFL++ commands prepare and check a seeded run; they do not start a campaign.
