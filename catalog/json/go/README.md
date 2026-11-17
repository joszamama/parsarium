# JSON / Go — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 1 verified standard APIs, 4 verified Docker harnesses.

Four Go JSON paths passed format-aware valid controls with source-scoped coverage and stable AFL++ feedback: json-iterator/go (18,454 Imported by), tidwall/gjson (10,420), ugorji/go/codec (10,142), and goccy/go-json (4,192). GJSON is a path-query parser whose harness calls its own ValidBytes first. go-codec is multi-format: the Imported by count measures the package across JSON, CBOR, MessagePack, binc and simple, and does not reveal JSON-specific adoption; its feedback is scoped to codec/json.* files. Five numeric leads remain unverified. Search is bounded to five pkg.go.dev queries of 100 results each. The Go standard encoding/json path is separate and unranked. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/go/json/ranking.md) · [Standard API inventory](../../../data/go/json/standard.json)

## Third-party parsers

- [github.com/json-iterator/go](github-com-json-iterator-go/README.md) — verified Docker harness
- [github.com/tidwall/gjson](github-com-tidwall-gjson/README.md) — verified Docker harness
- [github.com/ugorji/go/codec](github-com-ugorji-go-codec/README.md) — verified Docker harness
- [github.com/goccy/go-json](github-com-goccy-go-json/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/json.Unmarshal(\[\]byte, any)](standard/encoding-json-unmarshal-byte-any/README.md) — verified Docker harness
