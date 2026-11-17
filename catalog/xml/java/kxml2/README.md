# kxml2 — XML / Java

**Verified independent parser path.** Pinned Maven release `net.sf.kxml:kxml2:2.3.0`. Its [release POM](https://repo.maven.apache.org/maven2/net/sf/kxml/kxml2/2.3.0/kxml2-2.3.0.pom) states a BSD-style license for `org.kxml2` and public domain for the bundled XmlPull API. The [same-release source JAR](https://repo.maven.apache.org/maven2/net/sf/kxml/kxml2/2.3.0/kxml2-2.3.0-sources.jar) contains `KXmlParser.java`; [artifact hashes](../../../../projects/xml/java/kxml2/source-lock.json) pin it and the binary.

The harness creates `org.kxml2.io.KXmlParser`, enables namespace processing, calls `setInput` on a local stream, and consumes `next()` events. KXmlParser tokenizes the XML itself. It does not delegate to XPP3 MXParser, SAX, DOM, StAX, or JDK Xerces. The parser family is **kXML2 KXmlParser**. The published JAR lacks line tables, so its pinned same-release source is rebuilt with `javac -g --release 8` for line reporting.

Both [valid XML controls](../../../../controls/xml/) produce the expected namespace-aware projection. The first [control receipt](../../../../projects/xml/java/kxml2/verification.json) records 377 KXmlParser source lines. Three repeated valid probes per control were identical; the [differential receipt](../../../../fuzzing/afl-native/xml/java/kxml2/differential.json) records 29 changed parser features and 29 changed AFL tuples. The pinned JaCoCo agent includes `org.kxml2.io.*` only.

The saved [deps.dev snapshot](../../../../data/java/xml/registry-snapshot.json) gives 99 summed direct dependents across Maven releases and 62 at release `2.3.0`, its single-release maximum. This is package adoption within the Java XML cell. The legacy `kxml2:kxml2` Maven coordinate relocates to `net.sf.kxml:kxml2` and is not counted as a second parser path.

[Run this target](../../../../projects/xml/java/kxml2/README.md)
