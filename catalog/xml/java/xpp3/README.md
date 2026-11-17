# xpp3 — XML / Java

**Verified independent parser path.** Pinned Maven release `xpp3:xpp3:1.1.4c`. The [release POM](https://repo.maven.apache.org/maven2/xpp3/xpp3/1.1.4c/xpp3-1.1.4c.pom) identifies the Indiana University Extreme! Lab Software License 1.1.1 for the parser, public-domain XmlPull API, and Apache-1.1 for the bundled `QName` class. The [pinned source JAR](https://repo.maven.apache.org/maven2/xpp3/xpp3/1.1.4c/xpp3-1.1.4c-sources.jar) documents `XmlPullParser.setInput(InputStream, String)` and contains MXParser's source/license. [Artifact hashes](../../../../projects/xml/java/xpp3/source-lock.json) bind the release and source.

The harness constructs `org.xmlpull.mxp1.MXParser`, enables namespace processing, calls `setInput` on a local stream, and consumes `next()` events. This is XPP3's own tokenizer. It does not delegate to SAX, DOM, StAX, or the JDK Xerces parser. The parser family is **XPP3 MXParser**.

Both [valid XML controls](../../../../controls/xml/) produce the expected namespace-aware projection. The first [control receipt](../../../../projects/xml/java/xpp3/verification.json) records 677 MXParser source lines. Three repeated valid probes per control were identical; the [differential receipt](../../../../fuzzing/afl-native/xml/java/xpp3/differential.json) records 160 changed parser features and 160 changed AFL tuples. The pinned JaCoCo agent includes `org.xmlpull.mxp1.*` only.

The saved [deps.dev snapshot](../../../../data/java/xml/registry-snapshot.json) gives 285 summed direct dependents across Maven releases and 143 at release `1.1.4c`, its single-release maximum. The exact requested `1.1.3.4` artifact is unavailable from Maven Central; `1.1.4c` is a published release of the same coordinate. Package adoption is not a count of XML-specific calls.

[Run this target](../../../../projects/xml/java/xpp3/README.md)
