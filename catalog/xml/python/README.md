# XML / Python — pilot

**Status:** pilot_two_third_party_one_standard_verified_bounded_search_pending; incomplete. 2 verified third-party paths, 1 verified standard APIs, 2 verified Docker harnesses.

Two verified third-party paths (lxml and xmltodict) are selected from nine named PyPI/project-documentation leads. A bounded PyPI Simple Index search remains pending; seven leads are unresolved, so this is not a completed top-ten ranking. lxml uses source-built libxml2 2.15.4; xmltodict and the standard ElementTree path use Expat. Both lxml controls exercise valid UTF-8 XML 1.0 namespace structures without DOCTYPE, not full XML conformance. PyPI Stats package downloads are not XML-specific use. lxml AFL feedback excludes parser.c lines 8700-8720 because address-sensitive attribute hash lookups varied across identical valid replays.

[Ranking and search limits](../../../data/python/xml/ranking.md) · [Standard API inventory](../../../data/python/xml/standard.json)

## Third-party parsers

- [lxml](lxml/README.md) — verified Docker harness
- [xmltodict](xmltodict/README.md) — verified Docker harness

## Standard and runtime APIs

- [xml.etree.ElementTree.parse(BytesIO(local XML bytes)); getroot()](standard/xml-etree-elementtree-parse-bytesio-local-xml-bytes-getroot/README.md) — verified Docker harness
