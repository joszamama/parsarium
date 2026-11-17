# XML / Python — pilot

**Status:** pilot_three_third_party_one_standard_verified_bounded_search_pending; incomplete. 3 verified third-party paths, 1 verified standard APIs, 3 verified Docker harnesses.

Three verified third-party paths (lxml, beautifulsoup4 and xmltodict) are selected from nine named PyPI/project-documentation leads. A bounded PyPI Simple Index search remains pending; 6 leads are unresolved, so this is not a completed top-ten ranking. lxml uses source-built libxml2 2.15.4; beautifulsoup4's documented 'xml' builder runs on the same lxml 6.1.3/libxml2 2.15.4 pins (shared parser family, no independent XML tokenizer, recover=True); xmltodict and the standard ElementTree path use Expat. The lxml and beautifulsoup4 controls exercise valid UTF-8 XML 1.0 namespace structures without DOCTYPE, not full XML conformance. PyPI Stats package downloads are not XML-specific use; Beautiful Soup downloads are mostly HTML use. lxml and beautifulsoup4 AFL feedback excludes parser.c lines 8700-8720 because address-sensitive attribute hash lookups varied across identical valid replays.

[Ranking and search limits](../../../data/python/xml/ranking.md) · [Standard API inventory](../../../data/python/xml/standard.json)

## Third-party parsers

- [lxml](lxml/README.md) — verified Docker harness
- [beautifulsoup4](beautifulsoup4/README.md) — verified Docker harness
- [xmltodict](xmltodict/README.md) — verified Docker harness

## Standard and runtime APIs

- [xml.etree.ElementTree.parse(BytesIO(local XML bytes)); getroot()](standard/xml-etree-elementtree-parse-bytesio-local-xml-bytes-getroot/README.md) — verified Docker harness
