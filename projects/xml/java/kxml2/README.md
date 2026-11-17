# kxml2 — XML / Java

Pinned release: `net.sf.kxml:kxml2:2.3.0`. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json) · [AFL differential](../../../../fuzzing/afl-native/xml/java/kxml2/differential.json)

`org.kxml2.io.KXmlParser` reads local bytes through `setInput(InputStream, null)` with namespace processing enabled, then emits pull events through `next()`. KXmlParser is an independent XML tokenizer. The published release JAR lacks line tables, so the pinned same-release `KXmlParser.java` is rebuilt with debug lines and placed before the pinned JAR. JaCoCo and AFL feedback count only `org.kxml2.io` parser lines.

The valid controls are [`catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml) and [`order-default-ns.xml`](../../../../controls/xml/order-default-ns.xml). Both produce the expected namespace-aware result. The first covers 377 lines in `KXmlParser.java`. Three repeated source-line and AFL map probes per control were identical; the second control changed 29 parser features and 29 AFL tuples. A saved-queue replay of the two controls unions 398 parser lines.

## Run from the repository root

```sh
python3 parsarium.py build xml java kxml2
python3 parsarium.py run xml java kxml2 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java kxml2 CORPUS_DIR runs/xml-kxml2-replay
python3 parsarium.py afl build xml java kxml2
python3 parsarium.py afl prepare xml java kxml2 runs/xml-kxml2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

[API, parser-family and adoption evidence](../../../../catalog/xml/java/kxml2/README.md)
