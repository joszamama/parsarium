# JSON / Go — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 1 verified standard APIs, 3 verified Docker harnesses.

Three positive-signal Go JSON paths passed format-aware controls with parser source coverage and stable AFL++ feedback: json-iterator/go (18,454 Imported by), tidwall/gjson (10,420), and goccy/go-json (4,192). GJSON is a JSON path-query library; the harness calls its own ValidBytes before ParseBytes and traverses every Result, but its adoption metric does not identify general-purpose decoding use. The multi-format ugorji/go/codec (10,142) and five other numeric leads remain unverified; their rank is uncertain. Search is bounded to five pkg.go.dev queries of 100 results each. The Go standard encoding/json path is separate and unranked. The valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/go/json/ranking.md) · [Standard API inventory](../../../data/go/json/standard.json)

## Third-party parsers

- [github.com/json-iterator/go](github-com-json-iterator-go/README.md) — verified Docker harness
- [github.com/tidwall/gjson](github-com-tidwall-gjson/README.md) — verified Docker harness
- [github.com/goccy/go-json](github-com-goccy-go-json/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/json.Unmarshal(\[\]byte, any)](standard/encoding-json-unmarshal-byte-any/README.md) — verified Docker harness
