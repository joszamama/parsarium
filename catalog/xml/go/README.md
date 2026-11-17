# XML / Go — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 1 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: only the highest Imported-by XML parser lead (github.com/beevik/etree, 2,098) was built and control-verified. etree tokenizes with encoding/xml.Decoder.RawToken, so it shares the Go encoding/xml tokenizer family with the unranked standard path; only its tree building and namespace lookup are separate code. 15 further numeric leads are logged in leads.json and are not selected or ranked. Renderers, HTTP clients, Office/OOXML, SAML/xmldsig, JUnit, libvirt and AWS serializer hits were not treated as leads. The search covers the first 100 hits of six queries ('xml dom' returned 68 and 'xml reader' 28). Two small UTF-8 controls without DOCTYPE do not establish DTD, entity declaration, non-UTF-8 encoding, XML 1.1, or attribute-value normalization behaviour.

[Ranking and search limits](../../../data/go/xml/ranking.md) · [Standard API inventory](../../../data/go/xml/standard.json)

## Third-party parsers

- [github.com/beevik/etree](github-com-beevik-etree/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/xml.Decoder.Token()](standard/encoding-xml-decoder-token/README.md) — verified Docker harness
