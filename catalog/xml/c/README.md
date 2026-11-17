# XML / C — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two third-party paths (expat 2.10.0 and libxml2 2.15.4) were built, matched the exact namespace-resolved summary of both valid controls under LLVM source coverage, and have native AFL++ feedback with a stable valid-control differential. They are distinct parser families. expat leads libxml2 by 6,410 installs (2.2%) on the binary-package metric, a near tie. The Debian sourcemax table would invert the order (libxml2 source 61,109) only because the libxml2 source now builds libxml2-16 and the older libxml2 binary is no longer attributed to it, so binary runtime-library counts are the primary metric; libxml2-16 (9,413) is not added because hosts may have both. Popcon counts installations, mostly pulled in as dependencies, not direct parser use. Search was the Conan Center recipe-name substring 'xml' (9 hits, 1 of them a C XML parser) plus seven targeted C names; Conan and Debian miss vendored single-file parsers. The control oracle (controls/xml/check_controls.py) uses Python's pyexpat, the same family as expat but not libxml2, so the libxml2 match is a cross-family check. The expat harness pins XML_SetHashSalt so AFL++ maps are reproducible; libxml2 needed no such change. ISO C documents no XML API. Two valid UTF-8 controls without DOCTYPE do not establish DTD, entity, encoding, XML 1.1 or rejection behaviour.

[Ranking and search limits](../../../data/c/xml/ranking.md) · [Standard API inventory](../../../data/c/xml/standard.json)

## Third-party parsers

- [expat](expat/README.md) — verified Docker harness
- [libxml2](libxml2/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
