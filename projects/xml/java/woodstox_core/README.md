# Woodstox — XML / Java

`com.fasterxml.woodstox:woodstox-core` 7.3.0 is Apache-2.0 licensed. The adapter uses the pinned release's [`WstxInputFactory.createXMLStreamReader(InputStream)`](https://docs.oracle.com/en/java/javase/25/docs/api/java.xml/javax/xml/stream/XMLInputFactory.html#createXMLStreamReader(java.io.InputStream)) to parse local UTF-8 XML bytes with namespaces enabled. Its `XMLStreamReader` events produce expanded element names, namespace declarations, decoded text, depth, and sorted attributes. The [source lock](source-lock.json) pins the release jar, matching sources jar, and `stax2-api` 4.3.1 dependency. Woodstox implements its own StAX tokenizer and reader, separate from Xerces; `stax2-api` supplies interfaces only.

```sh
python3 parsarium.py build xml java woodstox_core
python3 parsarium.py run xml java woodstox_core controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml java woodstox_core
python3 parsarium.py afl prepare xml java woodstox_core runs/xml-woodstox-afl
python3 parsarium.py afl run runs/xml-woodstox-afl --check
```

The two valid namespace-aware controls match the independent expat structural oracle in `controls/xml/check_controls.py`. JaCoCo covers 815 lines in eight pinned `com.ctc.wstx.sr` parser source files, including `BasicStreamReader` and `StreamScanner`. AFL++ maps these lines into input-dependent feedback: three repeats per control agree, while the controls differ by 232 parser features and 230 AFL tuples. The `sr` scope excludes Woodstox's symbol-table cache, whose process-dependent paths made broader package coverage unstable. This tests the two XML 1.0 UTF-8 documents without DOCTYPE, not broader XML behavior. No fuzzing campaign is part of the receipt.
