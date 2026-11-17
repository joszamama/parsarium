# pugixml — XML / C++

Pinned release: `1.16` (GitHub release tarball, MIT, SHA-256 in [source-lock.json](source-lock.json)). [Manifest](manifest.json) · [verification receipt](verification.json)

The harness parses bytes with `pugi::xml_document::load_buffer` (`parse_default`, UTF-8). pugixml keeps qualified names and does no namespace processing, so the adapter resolves prefixes from in-scope `xmlns` attributes and rejects unbound prefixes and duplicate expanded attribute names. It reports the same namespace-resolved element and attribute names, declarations, depth and text as the Xerces-C++ path. Attributes are sorted per element to match the DOM adapters.

## Run from the repository root

```sh
python3 parsarium.py build xml cpp pugixml
python3 parsarium.py run xml cpp pugixml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp pugixml CORPUS_DIR runs/xml-pugixml-replay
python3 parsarium.py afl build xml cpp pugixml
python3 parsarium.py afl prepare xml cpp pugixml runs/xml-pugixml-afl
python3 scripts/verify_cpp_json_feedback.py --format xml --slug pugixml
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
