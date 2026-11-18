# JSON / Go — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 1 verified standard APIs, 10 verified Docker harnesses.

Ten Go JSON package paths pass two valid structure-aware controls with parser-source coverage and stable AFL++ feedback: json-iterator/go (18,454 Imported by), tidwall/gjson (10,420), ugorji/go/codec (10,142), goccy/go-json (4,192), mailru/easyjson/jlexer (3,424), bytedance/sonic (2,428), buger/jsonparser (2,171), valyala/fastjson (895), go-faster/jx (451), and segmentio/encoding/json (348). Sonic uses its own Go optdec plus native NEON parser on pinned linux/arm64 Go 1.27.1; Go line coverage and AFL feedback omit NEON assembly instructions. segmentio/encoding/json uses its own parse.go tokenizer and decoder; it imports encoding/json only for shared types. easyjson jlexer is used through its documented generic Lexer.Interface rather than generated code; its Imported by count mostly reflects generated code. go-faster/jx is a lightweight fork of json-iterator with rewritten decoder code and no import of json-iterator or encoding/json; its lineage is shared with the selected json-iterator path. GJSON and buger/jsonparser are path-query parsers; only GJSON has a full-document validator in its harness. go-codec is multi-format and its Imported by count is not JSON-specific. Ten paths reach the ceiling; go-structform/json and gojay remain unresolved leads and the k8s util/json and go-json-experiment paths share the standard encoding/json lineage, so ranks are among verified paths only. Search was bounded to five pkg.go.dev queries of 100 hits each. The standard encoding/json path remains separate and unranked. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/go/json/ranking.md) · [Standard API inventory](../../../data/go/json/standard.json)

## Third-party parsers

- [github.com/json-iterator/go](github-com-json-iterator-go/README.md) — verified Docker harness · [source repository](<https://github.com/json-iterator/go>) · [pkg.go.dev](<https://pkg.go.dev/github.com/json-iterator/go>)
- [github.com/tidwall/gjson](github-com-tidwall-gjson/README.md) — verified Docker harness · [source repository](<https://github.com/tidwall/gjson>) · [pkg.go.dev](<https://pkg.go.dev/github.com/tidwall/gjson>)
- [github.com/ugorji/go/codec](github-com-ugorji-go-codec/README.md) — verified Docker harness · [source repository](<https://github.com/ugorji/go>) · [pkg.go.dev](<https://pkg.go.dev/github.com/ugorji/go/codec>)
- [github.com/goccy/go-json](github-com-goccy-go-json/README.md) — verified Docker harness · [source repository](<https://github.com/goccy/go-json>) · [pkg.go.dev](<https://pkg.go.dev/github.com/goccy/go-json>)
- [github.com/buger/jsonparser](github-com-buger-jsonparser/README.md) — verified Docker harness · [source repository](<https://github.com/buger/jsonparser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/buger/jsonparser>)
- [github.com/valyala/fastjson](github-com-valyala-fastjson/README.md) — verified Docker harness · [source repository](<https://github.com/valyala/fastjson>) · [pkg.go.dev](<https://pkg.go.dev/github.com/valyala/fastjson>)
- [github.com/bytedance/sonic](github-com-bytedance-sonic/README.md) — verified Docker harness · [source repository](<https://github.com/bytedance/sonic>) · [pkg.go.dev](<https://pkg.go.dev/github.com/bytedance/sonic>)
- [github.com/segmentio/encoding/json](github-com-segmentio-encoding-json/README.md) — verified Docker harness · [source repository](<https://github.com/segmentio/encoding>) · [pkg.go.dev](<https://pkg.go.dev/github.com/segmentio/encoding/json>)
- [github.com/mailru/easyjson/jlexer](github-com-mailru-easyjson-jlexer/README.md) — verified Docker harness · [source repository](<https://github.com/mailru/easyjson>) · [pkg.go.dev](<https://pkg.go.dev/github.com/mailru/easyjson/jlexer>)
- [github.com/go-faster/jx](github-com-go-faster-jx/README.md) — verified Docker harness · [source repository](<https://github.com/go-faster/jx>) · [pkg.go.dev](<https://pkg.go.dev/github.com/go-faster/jx>)

## Standard and runtime APIs

- [encoding/json.Unmarshal(\[\]byte, any)](standard/encoding-json-unmarshal-byte-any/README.md) — verified Docker harness
