# XML / Python — pilot

**Status:** pilot_one_third_party_one_standard_verified_bounded_search_pending; incomplete. 1 verified third-party paths, 1 verified standard APIs, 1 verified Docker harnesses.

This is a one-parser pilot, not a completed registry search or top-ten claim. Nine named leads were inspected from PyPI/project documentation; the bounded PyPI Simple Index search remains pending. Eight third-party leads lack pinned control checks. The standard API inventory currently verifies ElementTree only; Expat, DOM and SAX API paths remain documented leads. xmltodict and ElementTree share the Expat syntax engine. The valid control exercises a common XML 1.0 subset, not full XML 1.0 conformance. PyPI Stats package downloads are not XML-specific use.

[Ranking and search limits](../../../data/python/xml/ranking.md) · [Standard API inventory](../../../data/python/xml/standard.json)

## Third-party parsers

- [xmltodict](xmltodict/README.md) — verified Docker harness

## Standard and runtime APIs

- [xml.etree.ElementTree.parse(BytesIO(local XML bytes)); getroot()](standard/xml-etree-elementtree-parse-bytesio-local-xml-bytes-getroot/README.md) — verified Docker harness
