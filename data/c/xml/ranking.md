# C XML parser pilot

The only verified third-party path in this pilot is
[`expat`](../../../projects/xml/c/expat/README.md) 2.10.0. Its documented API
(`XML_ParserCreateNS`, the element, namespace-declaration and character-data
handlers, `XML_Parse` over a local buffer) reported the exact namespace-resolved
summary of both valid controls. Its runtime library package `libexpat1` has
**297,134 Debian popcon installations** in the
[saved snapshot](registry-snapshot.json). That counts installations, mostly
pulled in as a dependency; it is an adoption proxy, not a count of programs that
call the parser.

## Primary within-cell adoption metric

Debian popcon installations of the lead's runtime library binary package,
captured 2026-11-17. The source-package (sourcemax) table is not used: the
libxml2 source now builds `libxml2-16`, so the older `libxml2` binary's
installations are no longer attributed to it.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [expat](https://libexpat.github.io/doc/api/latest/) | 2.10.0 | 297,134 | Namespace-resolved elements, attributes, declarations, depth and character data of one in-memory document | expat |

## Leads

One Conan recipe-name query (`xml`, 9 hits) and seven targeted C names. The
[leads](leads.json) record each one. None of these is a verified entry.

- libxml2 (`libxml2` 290,724; `libxml2-16` 9,413): independent family, second by
  6,410 installs. A scratch `xmlTextReader` build of 2.15.4 printed both control
  summaries, but it has no committed project or AFL++ overlay. Homebrew 365-day
  installs, a cross-check only, give the same order (expat 1,360,500; libxml2
  564,778).
- mxml (`libmxml1` 2,054): own tree parser; not built.
- libroxml, yxml, ezxml, sxmlc: no Debian package in the snapshot, so no
  primary value; not built.
- 8 hits are excluded: six C++ parsers, the libxml++ wrapper and xmlsec, both
  over libxml2.

This one-entry pilot is neither a top-ten ranking nor evidence that only one C
XML parser exists. The [cell record](cell.json) gives the remaining uncertainty
and the [standard-library finding](standard.json).
