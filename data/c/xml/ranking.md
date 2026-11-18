# C XML parser pilot

This pilot has seven verified third-party paths:
[`expat`](../../../projects/xml/c/expat/README.md) 2.10.0, [`libxml2`](../../../projects/xml/c/libxml2/README.md) 2.15.4, [`libxmlb`](../../../projects/xml/c/libxmlb/README.md) 0.3.30, [`ixml`](../../../projects/xml/c/ixml/README.md) (pupnp IXML) 22.2.1, [`mxml`](../../../projects/xml/c/mxml/README.md) (Mini-XML) 4.0.6, [`gdome2`](../../../projects/xml/c/gdome2/README.md) 0.8.1+debian-10 (a DOM over libxml2) and [`libnxml`](../../../projects/xml/c/libnxml/README.md) 0.18.6. expat's
documented API (`XML_ParserCreateNS`, the element, namespace-declaration and
character-data handlers, `XML_Parse` over a local buffer) and libxml2's
(`xmlReaderForMemory` over a local buffer, then the `xmlTextReaderRead` pull
loop) both reported the exact namespace-resolved summary of both valid controls.
Mini-XML's `mxmlLoadString` builds a tree of the same controls, but Mini-XML
does not implement XML namespaces: it returns names as written (`c:catalog`) and
keeps `xmlns` declarations as attributes. Its adapter resolves the expanded
names from that tree, and that summary matches too.
Their runtime library packages have **297,134** (`libexpat1`), **290,724** (`libxml2`), **130,663** (`libxmlb2`), **46,966** (`libixml11t64`), **2,054** (`libmxml1`), **518** (`libgdome2-0`) and **104** (`libnxml0t64`) Debian popcon installations in the
[saved snapshot](registry-snapshot.json). That counts installations,
mostly pulled in as a dependency; it is an adoption proxy, not a count of
programs that call the parser.

## Primary within-cell adoption metric

Debian popcon installations of the lead's runtime library binary package,
captured 2026-11-17 (`by_inst.gz`, SHA-256
`299486c46a56fc44b390058490a50b9f1250335c7cdf6f1e02b8cee0a212a802`). The
source-package (sourcemax) table is not used for ranking: the libxml2 source now
builds `libxml2-16`, so the older `libxml2` binary's installations are no
longer attributed to it.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [expat](https://libexpat.github.io/doc/api/latest/) | 2.10.0 | 297,134 | Namespace-resolved elements, attributes, declarations, depth and character data of one in-memory document | expat |
| 2 | [libxml2](https://gnome.pages.gitlab.gnome.org/libxml2/html/xmlreader_8h.html) | 2.15.4 | 290,724 | Namespace-resolved elements, attributes, declarations, depth and character data of one in-memory document | libxml2 |
| 3 | [libxmlb](https://github.com/hughsie/libxmlb/blob/0.3.30/src/xb-builder-source.c) | 0.3.30 | 130,663 | Raw-name element and attribute tree, depth and text of one in-memory document; no namespace URIs | GLib GMarkup |
| 4 | [ixml](https://github.com/pupnp/pupnp/blob/release-22.2.1/ixml/inc/ixml.h) | 22.2.1 | 46,966 | Raw-name element and attribute DOM, depth and text of one in-memory document; no namespace URIs | IXML (pupnp) |
| 5 | [mxml](https://www.msweet.org/mxml/mxml.html) | 4.0.6 | 2,054 | Element tree, attributes, depth and character data of one in-memory document; namespaces resolved by the adapter, not by Mini-XML | Mini-XML |
| 6 | [gdome2](https://sources.debian.org/src/gdome2/0.8.1%2Bdebian-10/gtk-doc/html/gdome2-gdomedomimplementation.html) | 0.8.1+debian-10 | 518 | Namespace-resolved DOM Level 2 elements, attributes, declarations, depth and text of one in-memory document | libxml2 (gdome2 DOM layer) |
| 7 | [libnxml](https://github.com/bakulf/libnxml/blob/0.18.6/src/nxml.h.in) | 0.18.6 | 104 | Raw-name element and attribute tree, depth and text of one in-memory document; no namespace URIs | nXML |

`libmxml1` is the Mini-XML 3.x library package; the pinned 4.0.6 is the
`mxml` source in Debian forky and sid. 1,842 of the 2,054 `libmxml1`
installations are in popcon's no-files column.

libxmlb has no tokenizer of its own: `xb_builder_source_load_xml` and `xb_builder_compile` feed the
document to GLib's GMarkup (`g_markup_parse_context_parse`, CDATA as text) and store the result in a
silo. Neither implements namespaces, so libxmlb is measured as a **raw-name path**: element and
attribute names as written, `xmlns` declarations as ordinary attributes, no URIs. Both valid controls
match Python expat in non-namespace mode ([oracle](../../../projects/xml/c/libxmlb/oracle.py)). The
pinned [libxmlb 0.3.30 release asset](https://github.com/hughsie/libxmlb/releases/tag/0.3.30)
(SHA-256 `2cb894b873aac5fc9e9b6228d4e795f7236d16e429ed2de8f95179a131be3a68`, LGPL-2.1-or-later) is built
with GLib 2.88.4 from source (SHA-256 `25fd169f3b2f91fe2391ad297883ce0fcf30c69fc789ffd1c9672d1332b1c5a8`).
The first control covers 1,381 libxmlb lines and 604 `gmarkup.c` lines; between the controls 53 GMarkup
and 8 libxmlb line starts differ. The AFL++ overlay instruments only `gmarkup.c` and libxmlb's
`xb-*.c` (allowlist checked with `nm`); its maps repeat exactly, 639 vs 653 tuples with 32 differing.
GMarkup is documented as an XML subset (no DTDs) and libxmlb drops comments and processing
instructions. GMarkup itself is not ranked: its source `glib2.0` builds all of GLib.

libnxml 0.18.6 ([tag archive](https://github.com/bakulf/libnxml/releases/tag/0.18.6), SHA-256
`c6de3c486f37c064eeae7d94e74f8dd25328e23effd8409a26a1170c19203ab4`, LGPL-2.1-or-later) has its own reader
and tree. `nxml_parse_buffer` always runs a namespace pass, but that pass also puts unprefixed
attributes in the default namespace, so libnxml is also measured as a raw-name path: the adapter
re-joins libnxml's stored prefix and local name and reports no URIs. Both valid controls match the
expat non-namespace oracle. The first control covers 720 libnxml lines (346 in `nxml_parser.c`); 143
line starts differ between the controls, and the AFL++ maps (393 vs 426 tuples, 53 differing) repeat
exactly. Its 104 installations are a very weak package signal.

pupnp's IXML 22.2.1 ([release asset](https://github.com/pupnp/pupnp/releases/tag/release-22.2.1), SHA-256
`11ac0f670aad96bd9c81cc84a6d4ae874a7b4b11073d5b88a03fd43efd097cc6`, BSD-3-Clause) is the DOM parser bundled
with the portable UPnP SDK; Debian ships it as its own runtime package (`libixml11t64`, `libixml10`,
`libixml22`), which is how the binary-name search found it. `ixmlParseBufferEx` builds a DOM whose node
names are the qualified names as written, with `xmlns` declarations kept as attributes. IXML also fills
namespace fields, but not conformantly on the controls (no default namespace below the prefixed catalog
root, `xmlns=""` not applied to its own element, no URIs on prefixed attributes), so it is measured as a
**raw-name path** against the same expat non-namespace oracle. It drops comments and processing
instructions. Only the IXML static library is built; the first control covers 1,428 IXML lines (908 in
`ixmlparser.c`) and the AFL++ maps (433 vs 449 tuples, 82 differing) repeat exactly over five runs.
Almost all of its installations come from UPnP/DLNA media software that depends on it.

gdome2 0.8.1+debian-10 ([Debian orig tarball](https://deb.debian.org/debian/pool/main/g/gdome2/), SHA-256
`f4bb80a2ef8e5fd9397ab8aa36d059d0b32e98c4bcf185c7952a7e3874d1d543`, with Debian's two source patches; LGPL-2.1-or-later)
is a C DOM Level 2 implementation over libxml2. `gdome_di_createDocFromMemory` parses with libxml2's `xmlParseMemory`;
gdome2's `namespaceURI`/`localName` accessors and the `xmlns` declaration attributes it exposes give the exact
namespace-resolved summary of both controls, so it is measured against the shared expat oracle. It is a **libxml2-family**
path, built over the same pinned libxml2 2.15.4: the first control covers 744 gdome2 and 3,207 libxml2 lines, 22 gdome2 and
334 libxml2 `parser.c` line starts differ between the controls, and the AFL++ maps (1,389 vs 1,490 tuples, 259 differing)
repeat exactly. Its 518 installations come from software that depends on it.

## Leads

One Conan recipe-name query (`xml`, 9 hits), seven targeted C names, every
Debian source name containing `xml` in the hashed sourcemax snapshot (306 hits,
all classified in the [snapshot](registry-snapshot.json): 5 C XML parser
libraries, 13 other C or tool packages, 21 C++ packages, 4 data packages and
263 other-language packages) and seven targeted Debian sources. A second Debian query takes binary-package names containing `xml`
in the primary-metric `by_inst` table (1,208 hits; the first 100 by installations are classified in the
snapshot): it adds pupnp's IXML and otherwise only selected runtimes, wrappers, tools, C++ modules and
other-language packages. In round 4 the remaining 1,108 hits were classified too
(`round_4_continuation` in the snapshot): libxmltok (expat 1.2) and libxml1 (libxml 1.x) are predecessors of the selected
expat and libxml2, libucw-xml is a lead, and libxmlbird and GXml are Vala libraries. Targeted lookups of C libraries with a
documented XML API whose binary names lack `xml` added gdome2. The
[leads](leads.json) record each candidate. Apart from the seven verified entries, none of them is verified.

Homebrew 365-day installs, a cross-check only, give the same order for expat,
libxml2 and mxml (1,360,500; 564,778; 127). `libxml2-16` (9,413) is not added
to libxml2's value because hosts may have both packages.

- GLib GMarkup: unranked. Its source `glib2.0` builds all of GLib, and Debian
  has no GMarkup-specific development package for the fallback rule. It is
  libxmlb's underlying parser.
- neon (libneon27t64 95,819) and APR-util (libaprutil1t64 76,853): documented generic XML APIs (`ne_xml` over libxml2,
  `apr_xml` over expat; neon passed both controls in a scratch build), but unranked by the GMarkup rule: their runtime and
  development packages are whole HTTP or utility libraries, not XML-specific.
- libxmltok (libxmltok1 143) is expat 1.2 and libxml1 (20) is libxml 1.x: predecessors of selected paths, excluded.
- iksemel (libiksemel3 4,375; source no longer in Debian): own parser, but it
  fails `order-default-ns.xml` — character references become `?` and attribute
  entities stay undecoded. It stays a lead.
- libroxml, yxml, ezxml, sxmlc: no Debian package in the snapshot, so no
  primary value; not built.
- Excluded: libgsf (schema-table wrapper over libxml2), qdbm (tokenizer helpers
  in a database library), xmlrpc-c and xmlrpc-epi (XML-RPC), libstrophe (XMPP),
  wbxml2 (binary XML), and 8 Conan hits (six C++ parsers, the libxml++ wrapper
  and xmlsec, both over libxml2).

This pilot is neither a top-ten ranking nor evidence that only these C
XML parsers exist. The [cell record](cell.json) gives the remaining uncertainty
and the [standard-library finding](standard.json).
