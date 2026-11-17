# sax — XML / JavaScript

Pinned release: `sax` 1.6.1, Blue Oak Model License 1.0.0. The npm release tarball is SHA-256 pinned in the [source lock](source-lock.json) and Dockerfile; that tarball includes `package/LICENSE.md`. The [upstream README](https://github.com/isaacs/sax-js/blob/v1.6.1/README.md) documents strict `sax.parser(true, { xmlns: true })`, `write().close()`, and a local file stream route through `createStream`.

The adapter reads a local file as bytes, performs strict UTF-8 decoding, and feeds the text to sax's strict namespace-aware SAX state machine. It returns expanded element and attribute names, namespace declarations, and decoded text. Both pinned valid controls match the independent Expat summary. The [manifest](manifest.json) and [base verification](verification.json) record the source pin, control result, and sax parser source-line coverage.

The [AFL++ overlay](../../../../fuzzing/afl-native/xml/javascript/sax/verification.json) maps executed sax parser source ranges into feedback tuples. Repeated control probes match and the second valid XML control changes both parser features and AFL tuples. These tuples are not comparable to native compiled edges.

From the repository root:

```sh
python3 parsarium.py build xml javascript sax
python3 parsarium.py run xml javascript sax controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml javascript sax
python3 parsarium.py afl prepare xml javascript sax runs/xml-sax-afl
python3 parsarium.py afl run runs/xml-sax-afl --check
```

The last command checks a prepared plan. It does not start a fuzzing campaign.
