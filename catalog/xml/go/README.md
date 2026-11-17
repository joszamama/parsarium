# XML / Go — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 1 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: the two highest Imported-by XML parser leads (etree 2,098; xmlquery 627) were built and control-verified. Both use the Go encoding/xml Decoder tokenizer, but build distinct trees. 14 further numeric leads remain unresolved and are not selected or ranked. The first 100 hits of six queries were captured (xml dom returned 68; xml reader 28). The two small valid UTF-8 XML 1.0 controls without DOCTYPE do not establish DTD, entity declaration, non-UTF-8 encoding, XML 1.1, or attribute-value normalization behaviour.

[Ranking and search limits](../../../data/go/xml/ranking.md) · [Standard API inventory](../../../data/go/xml/standard.json)

## Third-party parsers

- [github.com/beevik/etree](github-com-beevik-etree/README.md) — verified Docker harness
- [github.com/antchfx/xmlquery](github-com-antchfx-xmlquery/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/xml.Decoder.Token()](standard/encoding-xml-decoder-token/README.md) — verified Docker harness
