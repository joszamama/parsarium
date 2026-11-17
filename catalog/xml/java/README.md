# XML / Java — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 1 verified standard API, 3 verified third-party Docker harnesses.

Xerces, Woodstox, and Aalto are three independent third-party XML parser families with documented local input APIs, exact namespace-aware structural results on two valid controls, JaCoCo parser source lines, and stable input-dependent AFL++ feedback. The standard `javax.xml.parsers` path runs an OpenJDK Xerces fork and is counted separately. The primary ranking uses deps.dev direct dependents summed over releases. Ten documentation leads remain unresolved; the small UTF-8 controls without DOCTYPE do not establish DTD, schema, non-UTF-8, or XML 1.1 behavior.

[Ranking and search limits](../../../data/java/xml/ranking.md) · [Standard API inventory](../../../data/java/xml/standard.json)

## Third-party parsers

- [xercesImpl](xercesimpl/README.md) — verified Docker harness
- [woodstox-core](woodstox-core/README.md) — verified Docker harness
- [aalto-xml](aalto-xml/README.md) — verified Docker harness

## Standard and runtime APIs

- [javax.xml.parsers.DocumentBuilder.parse(InputStream)](standard/javax-xml-parsers-documentbuilder-parse-inputstream/README.md) — verified Docker harness
