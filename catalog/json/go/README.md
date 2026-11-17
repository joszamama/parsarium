# JSON / Go — pilot

**Status:** pilot_eight_selected_search_bounded; incomplete. 8 verified third-party paths, 1 verified standard APIs, 8 verified Docker harnesses.

Eight Go JSON package paths pass two valid structure-aware controls with parser-source coverage and stable AFL++ feedback: json-iterator/go (18,454 Imported by), tidwall/gjson (10,420), ugorji/go/codec (10,142), goccy/go-json (4,192), bytedance/sonic (2,428), buger/jsonparser (2,171), valyala/fastjson (895), and segmentio/encoding/json (348). Sonic uses its own Go optdec plus native NEON parser on pinned linux/arm64 Go 1.27.1; Go line coverage and AFL feedback omit NEON assembly instructions. segmentio/encoding/json uses its own parse.go tokenizer and decoder; it imports encoding/json only for shared types. GJSON and buger/jsonparser are path-query parsers; only GJSON has a full-document validator in its harness. go-codec is multi-format and its Imported by count is not JSON-specific. Two other numeric leads remain unverified, so ranks are among verified paths only. Search was bounded to five pkg.go.dev queries of 100 hits each. The standard encoding/json path remains separate and unranked. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/go/json/ranking.md) · [Standard API inventory](../../../data/go/json/standard.json)

## Third-party parsers

- [github.com/json-iterator/go](github-com-json-iterator-go/README.md) — verified Docker harness
- [github.com/tidwall/gjson](github-com-tidwall-gjson/README.md) — verified Docker harness
- [github.com/ugorji/go/codec](github-com-ugorji-go-codec/README.md) — verified Docker harness
- [github.com/goccy/go-json](github-com-goccy-go-json/README.md) — verified Docker harness
- [github.com/buger/jsonparser](github-com-buger-jsonparser/README.md) — verified Docker harness
- [github.com/valyala/fastjson](github-com-valyala-fastjson/README.md) — verified Docker harness
- [github.com/bytedance/sonic](github-com-bytedance-sonic/README.md) — verified Docker harness
- [github.com/segmentio/encoding/json](github-com-segmentio-encoding-json/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/json.Unmarshal(\[\]byte, any)](standard/encoding-json-unmarshal-byte-any/README.md) — verified Docker harness
