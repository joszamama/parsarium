# xom — XML / Java

**Verified third-party parsing path.** Pinned Maven release `xom:xom:1.4.6`, licensed under LGPL-2.1 in its [release POM](https://repo.maven.apache.org/maven2/xom/xom/1.4.6/xom-1.4.6.pom). The [Builder API](https://xom.nu/apidocs/nu/xom/Builder.html) documents `build(InputStream)` returning a `Document` from a local stream. The [source lock](../../../../projects/xml/java/xom/source-lock.json) records release JAR, source JAR, POM, runtime dependency and JDK source hashes.

XOM's `Builder.findParser` selects the OpenJDK internal Xerces SAX reader when Apache Xerces is absent. This is a distinct tree-builder package path with no independent XML tokenizer; it shares the Apache Xerces2-J family with JDOM2, dom4j, XMLBeans and the standard JDK path. The pinned release JAR lacks line tables, so its same-release sources are recompiled with `javac -g --release 8` and mapped to JaCoCo. The OpenJDK parser classes and matching sources are covered separately.

The two [valid XML controls](../../../../controls/xml/) exercise namespaces, attributes, decoded references, CDATA, comment, processing instruction, and namespace undeclaration. The first produces the expected [tree result](../../../../projects/xml/java/xom/verification.json) with 579 XOM lines and 3,488 underlying JDK Xerces lines. The second matches the shared XML oracle; repeated source-line feedback is stable and [72 AFL tuples differ](../../../../fuzzing/afl-native/xml/java/xom/differential.json).

The [deps.dev snapshot](../../../../data/java/xml/registry-snapshot.json) records 355 summed direct dependents across XOM Maven releases, with a maximum of 116 on release 1.2.5. This measures package adoption within the Java XML cell, not independent tokenizer adoption.

[Run this target](../../../../projects/xml/java/xom/README.md)
