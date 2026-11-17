# xom — XML / Java

Pinned release: `xom:xom:1.4.6` (LGPL-2.1). [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json) · [AFL differential](../../../../fuzzing/afl-native/xml/java/xom/differential.json)

`nu.xom.Builder.build(InputStream)` creates a namespace-aware XOM `Document` from local XML bytes. XOM builds the tree; the OpenJDK `java.xml` Xerces fork selected by `Builder.findParser` tokenizes XML. Both source groups are reported separately. The published XOM JAR has no line tables, so the pinned same-release sources are recompiled with debug lines for coverage and placed before the pinned release JAR. Apache Xerces is used only at compile time and is absent from the runtime classpath.

The valid controls are [`catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml) and [`order-default-ns.xml`](../../../../controls/xml/order-default-ns.xml). The first verifies the expected namespace-aware tree and covers 579 XOM lines plus 3,488 JDK Xerces lines. The second produces a different tree; six repeated AFL trace/map probes (three per control) were stable, with 72 parser source features and 72 AFL tuples differing.

## Run from the repository root

```sh
python3 parsarium.py build xml java xom
python3 parsarium.py run xml java xom controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xom CORPUS_DIR runs/xml-xom-replay
python3 parsarium.py afl build xml java xom
python3 parsarium.py afl prepare xml java xom runs/xml-xom-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

[API and parser-family evidence](../../../../catalog/xml/java/xom/README.md)
