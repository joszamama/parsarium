# JAVA × XML: selected parsers (pilot)

4 control-verified third-party paths and 1 control-verified standard path. The ceiling is ten; this pilot builds three independent XML parser engines and one wrapper path (dom4j) over the JDK Xerces fork, and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)). A dependent is counted once per release it depends on. The single-release maximum is recorded as a cross-check.

| Rank | Package | Release | Metric | Max single release | Parsed scope | Parser family |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | [xercesImpl](https://xerces.apache.org/xerces2-j/javadocs/xerces2/org/apache/xerces/parsers/DOMParser.html) | 2.12.2 | 2,474 | 549 (2.12.2) | Namespace-aware XML 1.0 into a W3C DOM | Apache Xerces2-J |
| 2 | [woodstox-core](https://central.sonatype.com/artifact/com.fasterxml.woodstox/woodstox-core/7.3.0) | 7.3.0 | 1,874 | 156 (7.0.0) | Namespace-aware XML 1.0 from a local InputStream into StAX events | Woodstox |
| 3 | [dom4j](https://central.sonatype.com/artifact/org.dom4j/dom4j/2.2.0) | 2.2.0 | 1,434 | 540 (2.1.1) | Namespace-aware XML 1.0 from a local InputStream into a dom4j Document via `SAXReader` | dom4j tree builder over the JAXP default SAX parser (Apache Xerces2-J, OpenJDK fork) |
| 4 | [aalto-xml](https://central.sonatype.com/artifact/com.fasterxml/aalto-xml/1.4.0) | 1.4.0 | 559 | 130 (1.0.0) | Namespace-aware XML 1.0 from a local InputStream into StAX events | Aalto |

Three coordinates score higher and are not parser engines: jackson-dataformat-xml (25,682) binds objects over a StAX reader, jsoup (7,010) is an HTML parser whose XML mode is not namespace-aware, and xstream (4,001) is a serializer over pluggable XML drivers. dom4j is ranked on the org.dom4j:dom4j coordinate alone (1,434 over 11 releases, rechecked unchanged on 2026-11-17). The legacy dom4j:dom4j 1.x coordinate (1,755) is the same project; it stays in the lead log and is not added or counted as a second path. dom4j has no tokenizer: `SAXReader` obtains its reader from `SAXParserFactory.newInstance()`, which on the pinned runtime is the OpenJDK java.xml Xerces fork. The protocol accepts it as a wrapper package path; it shares the Apache Xerces2-J family with xercesImpl and the standard path and is not an independent parser engine.

The xercesImpl release jar lacks line-number tables, so its pinned sources jar is recompiled with `javac -g --release 8`. The Woodstox, dom4j, and Aalto release jars include line tables; JaCoCo covers their pinned release classes directly and maps them to their same-release sources jars. For dom4j, the underlying JDK Xerces fork is instrumented as boot classes and reported separately against the jdk25u `jdk-25.0.5+8` sources (3,601 lines in 62 files on the first control). The [parser records](parsers.json) have the details.

## Standard API

`javax.xml.parsers.DocumentBuilder.parse(InputStream)` from a namespace-aware `DocumentBuilderFactory.newInstance()` on OpenJDK 25.0.5 ([docs](https://docs.oracle.com/en/java/javase/25/docs/api/java.xml/javax/xml/parsers/DocumentBuilder.html#parse(java.io.InputStream))). The default factory is `com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl`, a repackaged fork of Xerces2-J inside `java.xml`. **The xercesImpl and standard paths share the Apache Xerces2-J parser family.** They are separate, diverged code copies, not one binary. Sources come from the `jdk-25.0.5+8` tag of openjdk/jdk25u. Details in [standard.json](standard.json).

## Feedback

All five paths (four third-party and one standard) map JaCoCo source lines into AFL++ tuples. Repeated control runs give identical features, and `controls/xml/order-default-ns.xml` changes them ([afl-feedback.json](afl-feedback.json)). The differential output equals the expat oracle used for the Go and Python XML cells.

Woodstox feedback covers its StAX reader and scanner classes (815 pinned source lines on the first control). Aalto covers 1,427 pinned source lines, repeated valid controls are stable, and the two controls differ by 278 parser features and 277 AFL++ tuples. dom4j feedback is scoped to its own org.dom4j package lines (723 on the first control, mostly `SAXContentHandler`, `NamespaceStack`, `SAXReader`, and tree classes), not to the JDK Xerces fork; ten repeated traces per control were identical, and the two controls differ by 125 parser features and 125 AFL++ tuples. The Woodstox SymbolTable cache is outside that feedback scope because its process-dependent paths changed across identical replays; this does not exclude reader or scanner coverage.

## Lead log

Numeric leads looked up on deps.dev. Woodstox, dom4j (org.dom4j:dom4j), and Aalto were promoted to the verified ranking above; the remaining entries are unresolved or excluded. Maven Central text search ranks by relevance, so the search hits alone do not surface adoption.

| Lead | Version seen | Summed direct dependents | Max single release | Status | Note |
| --- | --- | ---: | ---: | --- | --- |
| [com.fasterxml.jackson.dataformat:jackson-dataformat-xml](https://central.sonatype.com/artifact/com.fasterxml.jackson.dataformat/jackson-dataformat-xml) | 2.23.0 | 25,682 | 725 | not a parser engine | XmlMapper object/tree binding over a StAX XMLStreamReader (Woodstox by default); a data-binding layer with no XML tokenizer of its own. Highest metric, but it ranks a Jackson format module, not an XML parser. |
| [org.jsoup:jsoup](https://central.sonatype.com/artifact/org.jsoup/jsoup) | 1.24.1 | 7,010 | 613 | not a parser engine | HTML5 parser; Parser.xmlParser() is a lenient non-namespace-aware tree builder, so it does not meet the namespace-aware XML 1.0 scope. Not run. |
| [com.thoughtworks.xstream:xstream](https://central.sonatype.com/artifact/com.thoughtworks.xstream/xstream) | 1.4.21 | 4,001 | 355 | not a parser engine | Object serialization library over pluggable XML drivers (XPP3, StAX, DOM); no XML tokenizer of its own. Not run. |
| [dom4j:dom4j](https://central.sonatype.com/artifact/dom4j/dom4j) | 20040902.021138 | 1,755 | 1,566 | unresolved | Legacy dom4j 1.x coordinate of the same dom4j project as the verified org.dom4j:dom4j 2.2.0 path; not counted as a second path and its metric is not added to org.dom4j:dom4j. SAXReader uses the same JAXP SAX delegation. Control not run. |
| [org.apache.xmlbeans:xmlbeans](https://central.sonatype.com/artifact/org.apache.xmlbeans/xmlbeans) | 5.4.1 | 1,433 | 319 | unresolved | Schema-bound XML binding; XmlObject.Factory.parse(InputStream) parses through its own Piccolo-derived/SAX layer. Control not run. |
| [org.jdom:jdom2](https://central.sonatype.com/artifact/org.jdom/jdom2) | 2.0.6.1 | 968 | 451 | unresolved | SAXBuilder.build(InputStream) builds a JDOM tree over a JAXP SAX parser (JDK Xerces fork by default); no tokenizer of its own. Control not run. |
| [org.codehaus.woodstox:stax2-api](https://central.sonatype.com/artifact/org.codehaus.woodstox/stax2-api) | 4.3.2 | 875 | 214 | not a parser engine | StAX2 API interfaces only; implemented by Woodstox/Aalto. Not a parser. |
| [org.jdom:jdom](https://central.sonatype.com/artifact/org.jdom/jdom) | 2.0.2 | 682 | 276 | unresolved | JDOM 1.x/2.0.2 coordinate; same SAXBuilder-over-JAXP design as jdom2. Control not run. |
| [org.codehaus.woodstox:woodstox-core-asl](https://central.sonatype.com/artifact/org.codehaus.woodstox/woodstox-core-asl) | 4.4.1 | 682 | 295 | unresolved | Woodstox 4.x under the old Codehaus coordinate; same parser family as woodstox-core. Control not run. |
| [com.sun.xml.fastinfoset:FastInfoset](https://central.sonatype.com/artifact/com.sun.xml.fastinfoset/FastInfoset) | 2.1.1 | 547 | 203 | not a parser engine | Binary Fast Infoset (ITU-T X.891) codec, not a parser for textual XML 1.0. |
| [xom:xom](https://central.sonatype.com/artifact/xom/xom) | 1.4.6 | 355 | 116 | unresolved | nu.xom.Builder.build(InputStream) builds a tree over an XMLReader (Xerces when present, else JDK); no tokenizer of its own. Control not run. |
| [xpp3:xpp3](https://central.sonatype.com/artifact/xpp3/xpp3) | 1.1.3.4 | 285 | 143 | unresolved | XmlPullParser implementation (MXParser) with its own tokenizer; old 2006-era release line. Control not run. |
| [net.sf.kxml:kxml2](https://central.sonatype.com/artifact/net.sf.kxml/kxml2) | 2.3.0 | 99 | 62 | unresolved | XmlPullParser implementation (KXmlParser) with its own tokenizer, used on Android. Control not run. |
| [com.ximpleware:vtd-xml](https://central.sonatype.com/artifact/com.ximpleware/vtd-xml) | 2.13.4 | 29 | 13 | unresolved | VTDGen.setDoc(byte[]).parse(true) non-extractive token index; GPL-2.0. Control not run. |

Queries: `xml`, `xml parser`, `dom4j`, `jdom`, `xerces`, `stax`; limit 100 each; 346 hits, 345 unique.
