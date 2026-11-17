# aalto-xml — XML / Java

Pinned release: `com.fasterxml:aalto-xml:1.4.0` (Apache-2.0). [Manifest](manifest.json) · [source lock](source-lock.json) · [container receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/xml/java/aalto_xml/verification.json)

The adapter gives a local XML byte stream to Aalto's documented `InputFactoryImpl.createXMLStreamReader(InputStream)` and consumes StAX events. Aalto has its own `StreamReaderImpl`, `Utf8Scanner`, and `StreamScanner`; `stax2-api` contributes interfaces. This is independent of the selected Woodstox and Xerces engines. Namespace processing is enabled, DTD and external-entity support are disabled, and entity references in the valid controls are expanded.

The two valid UTF-8 XML 1.0 controls exercise prefixed and default namespaces, attributes, character references, CDATA, comments, a processing instruction, and namespace undeclaration. The namespace-aware structural outputs match the expat control oracle. The first control covered 1,427 pinned Aalto source lines. Three repeated probes of each valid control gave identical parser features and AFL++ maps; the controls differed by 278 parser features and 277 AFL++ tuples. This evidence does not establish XML 1.1, DTD, schema, or other encodings.

## Run from the repository root

```sh
python3 parsarium.py build xml java aalto_xml
python3 parsarium.py run xml java aalto_xml controls/xml/catalog-ns.xml
python3 parsarium.py run xml java aalto_xml controls/xml/order-default-ns.xml
python3 parsarium.py afl build xml java aalto_xml
python3 parsarium.py afl prepare xml java aalto_xml runs/xml-aalto_xml-afl
python3 parsarium.py afl run runs/xml-aalto_xml-afl --check
```

The AFL++ preparation creates a seeded run directory and does not start a campaign.
