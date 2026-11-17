# GO × JSON: selected parsers (pilot)

2 control-verified third-party paths selected. The ceiling is ten; this pilot builds the two highest-adoption general-purpose JSON decoder leads and does not pad the selection. gjson (10,420) and ugorji/go/codec (10,142) sit between them by count but were passed over: gjson is a non-validating path-query API, and the codec count covers several binary formats besides JSON. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/json-iterator/go](https://pkg.go.dev/github.com/json-iterator/go@v1.1.12) | v1.1.12 | 18,454 | RFC 8259 JSON text into interface{} | json-iterator Iterator parser |
| 2 | [github.com/goccy/go-json](https://pkg.go.dev/github.com/goccy/go-json@v0.12.0) | v0.12.0 | 4,192 | RFC 8259 JSON text into interface{} | go-json compiled decoder |

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [encoding/json.Unmarshal([]byte, any)](https://pkg.go.dev/encoding/json@go1.27.1#Unmarshal) | Go 1.27.1 | Go encoding/json v2 / jsontext decoder |

In the default Go 1.27.1 build, the v1 `encoding/json` API delegates to `encoding/json/v2` and `encoding/json/jsontext`. `encoding/json` itself shows 1,523,261 importers but stays outside the third-party ranking.

## Lead log

Numeric leads from the same snapshot, not verified and not selected. Loggers, JWT, JSON-RPC, schema, and protobuf JSON mapping hits were not treated as parser leads.

| Lead | Version seen | Imported by | Status |
| --- | --- | ---: | --- |
| [github.com/tidwall/gjson](https://pkg.go.dev/github.com/tidwall/gjson) | v1.20.4 | 10,420 | Path query API gjson.GetBytes/Parse over bytes; documented as not validating JSON (gjson.Valid is a separate call), so not taken as the next general-purpose decoder. Not run. |
| [github.com/ugorji/go/codec](https://pkg.go.dev/github.com/ugorji/go/codec) | v1.3.2 | 10,142 | Multi-format codec (msgpack, cbor, binc, simple, json); its Imported by count covers every format, so it is not comparable with JSON-only packages. JSON decoder path not run. |
| [github.com/mailru/easyjson/jlexer](https://pkg.go.dev/github.com/mailru/easyjson/jlexer) | v0.9.2 | 3,424 | Lexer for generated easyjson code; a generic local-bytes decode into an untyped value remains unchecked. |
| [github.com/bytedance/sonic](https://pkg.go.dev/github.com/bytedance/sonic) | v1.15.5 | 2,428 | Documentation describes JIT/SIMD paths and an encoding/json-compatible fallback on unsupported platforms; linux/arm64 parser family remains unchecked. |
| [github.com/buger/jsonparser](https://pkg.go.dev/github.com/buger/jsonparser) | v1.6.1 | 2,171 | Byte-slice Get/ArrayEach/ObjectEach parser; control not run in this pilot. |
| [k8s.io/apimachinery/pkg/util/json](https://pkg.go.dev/k8s.io/apimachinery/pkg/util/json) | v0.37.2 | 2,062 | Wrapper over sigs.k8s.io/json, an encoding/json fork; would share the Go encoding/json lineage. Not run. |
| [github.com/valyala/fastjson](https://pkg.go.dev/github.com/valyala/fastjson) | v1.6.10 | 895 | Parser.ParseBytes over bytes; control not run in this pilot. |

Queries: `json`, `json parser`, `json decoder`, `json unmarshal`, `json iterator`; limit 100 each; 500 hits, 474 unique.
