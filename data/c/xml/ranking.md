# C XML parser pilot

This pilot has two verified third-party paths from different parser families:
[`expat`](../../../projects/xml/c/expat/README.md) 2.10.0 and
[`libxml2`](../../../projects/xml/c/libxml2/README.md) 2.15.4. expat's
documented API (`XML_ParserCreateNS`, the element, namespace-declaration and
character-data handlers, `XML_Parse` over a local buffer) and libxml2's
(`xmlReaderForMemory` over a local buffer, then the `xmlTextReaderRead` pull
loop) both reported the exact namespace-resolved summary of both valid controls.
Their runtime library packages have **297,134** (`libexpat1`) and **290,724**
(`libxml2`) Debian popcon installations in the
[saved snapshot](registry-snapshot.json), a 2.2% gap. That counts installations,
mostly pulled in as a dependency; it is an adoption proxy, not a count of
programs that call the parser.

## Primary within-cell adoption metric

Debian popcon installations of the lead's runtime library binary package,
captured 2026-11-17. The source-package (sourcemax) table is not used: the
libxml2 source now builds `libxml2-16`, so the older `libxml2` binary's
installations are no longer attributed to it.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [expat](https://libexpat.github.io/doc/api/latest/) | 2.10.0 | 297,134 | Namespace-resolved elements, attributes, declarations, depth and character data of one in-memory document | expat |
| 2 | [libxml2](https://gnome.pages.gitlab.gnome.org/libxml2/html/xmlreader_8h.html) | 2.15.4 | 290,724 | Namespace-resolved elements, attributes, declarations, depth and character data of one in-memory document | libxml2 |

## Leads

One Conan recipe-name query (`xml`, 9 hits) and seven targeted C names. The
[leads](leads.json) record each one. Apart from the two verified entries, none of them is verified.

Homebrew 365-day installs, a cross-check only, give the same order for the two
verified entries (expat 1,360,500; libxml2 564,778). `libxml2-16` (9,413) is not
added to libxml2's value because hosts may have both packages.

- mxml (`libmxml1` 2,054): own tree parser; not built.
- libroxml, yxml, ezxml, sxmlc: no Debian package in the snapshot, so no
  primary value; not built.
- 8 hits are excluded: six C++ parsers, the libxml++ wrapper and xmlsec, both
  over libxml2.

This two-entry pilot is neither a top-ten ranking nor evidence that only two C
XML parser exists. The [cell record](cell.json) gives the remaining uncertainty
and the [standard-library finding](standard.json).
