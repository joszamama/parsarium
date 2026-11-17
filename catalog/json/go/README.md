# JSON / Go — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 1 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two general-purpose JSON decoders were built and control-verified: github.com/json-iterator/go (18,454 Imported by) and github.com/goccy/go-json (4,192). gjson (10,420) was passed over as a non-validating path-query API and ugorji/go/codec (10,142) as a multi-format codec whose Imported by count is not JSON-specific. Seven further numeric leads are logged in leads.json and are not selected or ranked. Non-parser hits such as loggers, JWT, JSON-RPC, and protobuf JSON mappers were not treated as leads. Valid nested-object and nested-array controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/go/json/ranking.md) · [Standard API inventory](../../../data/go/json/standard.json)

## Third-party parsers

- [github.com/json-iterator/go](github-com-json-iterator-go/README.md) — verified Docker harness
- [github.com/goccy/go-json](github-com-goccy-go-json/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/json.Unmarshal(\[\]byte, any)](standard/encoding-json-unmarshal-byte-any/README.md) — verified Docker harness
