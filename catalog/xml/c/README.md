# XML / C — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Pilot cell: three third-party paths (expat 2.10.0, libxml2 2.15.4 and Mini-XML 4.0.6) were built, matched the exact namespace-resolved summary of both valid controls under LLVM source coverage, and have native AFL++ feedback with a stable valid-control differential. They are three distinct parser families. expat leads libxml2 by 6,410 installs (2.2%) on the binary-package metric, a near tie; mxml is two orders of magnitude lower (2,054, 1,842 of them in popcon's no-files column). The Debian sourcemax table would invert the first two (libxml2 source 61,109) only because the libxml2 source now builds libxml2-16 and the older libxml2 binary is no longer attributed to it, so binary runtime-library counts are the primary metric; libxml2-16 (9,413) is not added because hosts may have both. mxml's value is the 3.x soname libmxml1; the pinned 4.0.6 is Debian forky/sid's mxml source, and its libmxml4 binary has no row in the saved snapshot. Mini-XML does not implement Namespaces in XML: it returns prefix:local names and keeps xmlns declarations as attributes, so its expanded names, declaration counts and URIs are computed by the adapter from mxml's tree, not by the package. Popcon counts installations, mostly pulled in as dependencies, not direct parser use. Search was the Conan Center recipe-name substring 'xml' (9 hits, 1 of them a C XML parser) plus seven targeted C names; Conan and Debian miss vendored single-file parsers. The control oracle (controls/xml/check_controls.py) uses Python's pyexpat, the same family as expat but not libxml2 or Mini-XML, so those matches are cross-family checks. The expat harness pins XML_SetHashSalt so AFL++ maps are reproducible; libxml2 and mxml needed no such change. ISO C documents no XML API. Two valid UTF-8 controls without DOCTYPE do not establish DTD, entity, encoding, XML 1.1 or rejection behaviour.

[Ranking and search limits](../../../data/c/xml/ranking.md) · [Standard API inventory](../../../data/c/xml/standard.json)

## Third-party parsers

- [expat](expat/README.md) — verified Docker harness
- [libxml2](libxml2/README.md) — verified Docker harness
- [mxml](mxml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
