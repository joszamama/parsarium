# JSON / Go — pilot

**Status:** pilot_six_selected_search_bounded; incomplete. 6 verified third-party paths, 1 verified standard APIs, 6 verified Docker harnesses.

Six Go JSON package paths pass two valid structure-aware controls with parser-source coverage and stable AFL++ feedback: json-iterator/go (18,454 Imported by), tidwall/gjson (10,420), ugorji/go/codec (10,142), goccy/go-json (4,192), buger/jsonparser (2,171), and valyala/fastjson (895). GJSON and buger/jsonparser are path-query parsers; only GJSON has a full-document validator in its harness. go-codec is multi-format and its Imported by count is not JSON-specific. The higher-use sonic lead (2,428) and two other numeric leads remain unverified, so ranks are among verified paths only. Search was bounded to five pkg.go.dev queries of 100 hits each. The standard encoding/json path remains separate and unranked. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/go/json/ranking.md) · [Standard API inventory](../../../data/go/json/standard.json)

## Third-party parsers

- [github.com/json-iterator/go](github-com-json-iterator-go/README.md) — verified Docker harness
- [github.com/tidwall/gjson](github-com-tidwall-gjson/README.md) — verified Docker harness
- [github.com/ugorji/go/codec](github-com-ugorji-go-codec/README.md) — verified Docker harness
- [github.com/goccy/go-json](github-com-goccy-go-json/README.md) — verified Docker harness
- [github.com/buger/jsonparser](github-com-buger-jsonparser/README.md) — verified Docker harness
- [github.com/valyala/fastjson](github-com-valyala-fastjson/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/json.Unmarshal(\[\]byte, any)](standard/encoding-json-unmarshal-byte-any/README.md) — verified Docker harness
