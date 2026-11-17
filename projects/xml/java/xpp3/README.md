# xpp3 — XML / Java

Pinned release: `xpp3:xpp3:1.1.4c`. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json) · [AFL differential](../../../../fuzzing/afl-native/xml/java/xpp3/differential.json)

`org.xmlpull.mxp1.MXParser` reads local bytes through `setInput(InputStream, null)` with namespace processing enabled, then emits pull events through `next()`. MXParser is an independent XML tokenizer. JaCoCo tracks its pinned release classes against the same-release sources jar; API and harness lines are outside the parser source prefix.

The valid controls are [`catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml) and [`order-default-ns.xml`](../../../../controls/xml/order-default-ns.xml). Both produce the expected namespace-aware result. The first covers 677 lines in `MXParser.java`. Three repeated source-line and AFL map probes per control were identical, while the second control changed 160 parser features and 160 AFL tuples. A saved-queue replay of the two controls unions 772 parser lines.

The requested exact version `1.1.3.4` is not published at Maven Central (JAR, sources, and POM returned 404 on 2026-11-17). This project pins the published `1.1.4c` release of the same coordinate, which has the highest single-release direct-dependent count in the saved deps.dev snapshot.

## Run from the repository root

```sh
python3 parsarium.py build xml java xpp3
python3 parsarium.py run xml java xpp3 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xpp3 CORPUS_DIR runs/xml-xpp3-replay
python3 parsarium.py afl build xml java xpp3
python3 parsarium.py afl prepare xml java xpp3 runs/xml-xpp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

[API, parser-family and adoption evidence](../../../../catalog/xml/java/xpp3/README.md)
