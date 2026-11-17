# XML / Java — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 1 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: only the highest-adoption Java XML parser engine lead (xerces:xercesImpl 2.12.2, 2,474 deps.dev direct dependents summed over all releases) was built and control-verified. jackson-dataformat-xml, jsoup and xstream score higher but are a data-binding layer, an HTML parser and a serializer, and are logged as non-parser leads. dom4j (both coordinates summed: 3,189) and JDOM are tree builders over a JAXP SAX parser that defaults to the JDK Xerces fork, so they have no tokenizer of its own. The standard javax.xml.parsers path runs OpenJDK's internal repackaged Xerces fork, so both verified Java XML paths share the Apache Xerces2-J family; they are separate, diverged code copies. The xercesImpl release jar has no line tables, so its pinned sources jar is recompiled with -g for line coverage. DOM keeps no attribute order, so attributes are reported sorted per element. Maven Central text search ranks by relevance, not adoption; leads were looked up directly on deps.dev. Two small UTF-8 controls without DOCTYPE do not establish DTD, entity, schema, non-UTF-8 or XML 1.1 behaviour.

[Ranking and search limits](../../../data/java/xml/ranking.md) · [Standard API inventory](../../../data/java/xml/standard.json)

## Third-party parsers

- [xercesImpl](xercesimpl/README.md) — verified Docker harness

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
