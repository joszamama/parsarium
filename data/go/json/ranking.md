# GO × JSON: selected parsers (pilot)

10 control-verified third-party paths selected. The ceiling is ten. The cell is at its ceiling. GJSON is a JSON path-query parser: the harness uses its own full-document validation before traversing the parsed Result tree. go-codec is a multi-format package, so its Imported by count covers several formats and does not measure JSON-specific use. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/json-iterator/go](https://pkg.go.dev/github.com/json-iterator/go@v1.1.12) | v1.1.12 | 18,454 | RFC 8259 JSON text into interface{} | json-iterator Iterator parser |
| 2 | [github.com/tidwall/gjson](https://pkg.go.dev/github.com/tidwall/gjson@v1.20.4) | v1.20.4 | 10,420 | Validated JSON byte slice traversed through Result nodes | GJSON path-query parser |
| 3 | [github.com/ugorji/go/codec](https://pkg.go.dev/github.com/ugorji/go/codec@v1.3.2) | v1.3.2 | 10,142 | JSON via JsonHandle into untyped values | go-codec JSON decoder |
| 4 | [github.com/goccy/go-json](https://pkg.go.dev/github.com/goccy/go-json@v0.12.0) | v0.12.0 | 4,192 | RFC 8259 JSON text into interface{} | go-json compiled decoder |
| 5 | [github.com/mailru/easyjson/jlexer](https://pkg.go.dev/github.com/mailru/easyjson@v0.9.2/jlexer#Lexer.Interface) | v0.9.2 | 3,424 | Complete local JSON bytes decoded by Lexer.Interface into untyped Go values | easyjson jlexer own Go tokenizer |
| 6 | [github.com/bytedance/sonic](https://pkg.go.dev/github.com/bytedance/sonic@v1.15.5#Unmarshal) | v1.15.5 | 2,428 | Complete local JSON bytes into untyped Go values | Sonic optimized arm64 Go optdec over native NEON parser |
| 7 | [github.com/buger/jsonparser](https://pkg.go.dev/github.com/buger/jsonparser@v1.6.1) | v1.6.1 | 2,171 | Local JSON bytes traversed with Get/ObjectEach/ArrayEachErr | jsonparser byte scanner |
| 8 | [github.com/valyala/fastjson](https://pkg.go.dev/github.com/valyala/fastjson@v1.6.10#Parser.ParseBytes) | v1.6.10 | 895 | Complete local JSON bytes decoded into a Value tree | fastjson own Go parser |
| 9 | [github.com/go-faster/jx](https://pkg.go.dev/github.com/go-faster/jx@v1.2.0#DecodeBytes) | v1.2.0 | 451 | Complete local JSON bytes walked with the jx Decoder into untyped Go values | go-faster/jx own Go decoder (lightweight json-iterator fork) |
| 10 | [github.com/segmentio/encoding/json](https://pkg.go.dev/github.com/segmentio/encoding/json@v0.5.4#Unmarshal) | v0.5.4 | 348 | Complete local JSON bytes decoded into untyped Go values | segmentio/encoding/json own Go parser |

GJSON has a documented `ParseBytes([]byte)` API but does not validate input on its own. The harness calls its own `ValidBytes([]byte)` first, then traverses `Result.ForEach` over every object and array. Both valid controls pass; the second changes 39 GJSON source features and 39 AFL tuples under stable repeats. Its Imported by count is package adoption, not evidence of general-purpose JSON decoding.

go-codec uses `NewDecoderBytes(data, &JsonHandle{})` and its own JSON reader. The two valid controls pass. Its AFL feedback includes only covered `codec/json.*` parser source files: 258 control features and 278 AFL tuples, with stable repeats and a three-feature/three-tuple change on the valid array. The package metric is labeled as whole-package adoption and must not be read as JSON-specific popularity.

buger/jsonparser is a path-query parser. The adapter recursively walks both valid controls using `Get`, `ObjectEach`, and `ArrayEachErr`; it does not claim full-document validation on arbitrary input. The second control produces the expected array result and changes nine parser source features and nine AFL tuples under stable repeats. Sonic (2,428) now ranks above buger/jsonparser among verified paths.

fastjson uses the documented `Parser.ParseBytes` API and traverses the resulting `Value` tree. The complete nested object and array controls match the independent expected summaries. Go coverage reaches 257 lines in its pinned source; stable repeated controls differ by 15 parser source features and 15 AFL tuples. Its 895 Imported by count ranks eighth among verified paths.

Sonic v1.15.5 uses its own decoder on pinned Linux arm64 / Go 1.27.1: the harness checks `sonic.APIKind == sonic.UseSonicJSON`. `internal/decoder/api/decoder_arm64.go` routes to `optdec.Decode`, and `optdec` calls the native NEON parser. The object control covers 289 `optdec` Go lines; repeated source-scoped AFL++ feedback differs by 35 Go parser blocks and 35 tuples on the valid nested-array control. NEON assembly instructions are outside Go line coverage and feedback here.

segmentio/encoding/json uses the documented `Unmarshal([]byte, any)` API into `*any`. In the pinned v0.5.4 source, `Unmarshal` calls the package's own `Parse`, and `decodeInterface` tokenizes with `parseValue` in `parse.go` before building maps and slices in `decode.go`. It imports `encoding/json` only for shared types (`RawMessage`, `Number`, error and interface aliases) and for `Compact`/`HTMLEscape`/`Indent`, which the harness does not call. Both valid controls match an independent Python `json` oracle. Go coverage reaches 367 lines in five package files (217 in `parse.go`); stable repeated controls differ by 14 parser source features and 14 AFL tuples. Its 348 Imported by count, from the same snapshot, ranks tenth among verified paths.

easyjson's jlexer is the lexer that easyjson-generated code calls. The harness does not use generated code: it calls the documented generic `Lexer{Data: data}.Interface()`, then `Consumed()` and `Error()`, so trailing non-whitespace is rejected. `Interface` tokenizes with jlexer's own `FetchToken`/`fetchString`/`fetchNumber` scanner and builds maps and slices; the package imports `encoding/json` only for `json.Number` and for `json.Valid` inside `SkipRecursive`, neither of which this path calls. Both valid controls match an independent Python `json` oracle. Go coverage reaches 212 lines in the pinned jlexer package (211 in `lexer.go`); stable repeated controls differ by 6 parser source features and 6 AFL tuples. Its 3,424 Imported by count ranks fifth among verified paths, but most importers are easyjson-generated files, so it measures jlexer adoption rather than use of `Interface`.

go-faster/jx describes itself as a lightweight fork of json-iterator, and its LICENSE keeps the json-iterator copyright, so it shares lineage with the selected json-iterator path. It does not import json-iterator or `encoding/json` in non-test files, and its decoder was rewritten: only 55 of 933 distinct non-test source lines longer than 25 characters also occur in json-iterator v1.1.12. The harness calls the documented `DecodeBytes` and walks values with `Next`, `Obj`, `Arr`, `Str`, `Float64`, `Bool` and `Null`; a final `Skip` must return `io.EOF`. Both valid controls match an independent Python `json` oracle. Go coverage reaches 355 lines in twelve jx files (120 in `dec_str.go`, 7 of them from a package init table); stable repeated controls differ by 38 parser source features and 38 AFL tuples. Its 451 Imported by count ranks ninth among verified paths.

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [encoding/json.Unmarshal([]byte, any)](https://pkg.go.dev/encoding/json@go1.27.1#Unmarshal) | Go 1.27.1 | Go encoding/json v2 / jsontext decoder |

In the default Go 1.27.1 build, the v1 `encoding/json` API delegates to `encoding/json/v2` and `encoding/json/jsontext`. `encoding/json` itself shows 1,523,261 importers but stays outside the third-party ranking.

## Lead log

Numeric leads from the same snapshot, not verified and not selected. Loggers, JWT, JSON-RPC, schema, and protobuf JSON mapping hits were not treated as parser leads.

| Lead | Version seen | Imported by | Status |
| --- | --- | ---: | --- |
| [k8s.io/apimachinery/pkg/util/json](https://pkg.go.dev/k8s.io/apimachinery/pkg/util/json) | v0.37.2 | 2,062 | unresolved shared family: Not run. In v0.37.2, pkg/util/json Unmarshal calls sigs.k8s.io/json UnmarshalCaseSensitivePreserveInts (go.mod pins sigs.k8s.io/json v0.0.0-20250730193827-2d320260d730), whose internal/golang/encoding/json is a patched copy of the Go encoding/json v1 decoder (scanner.go keeps the Go Authors header). It shares the encoding/json lineage of the separately inventoried standard API, so an independent parser was preferred. |
| [github.com/crossplane/upjet/v2/pkg/resource/json](https://pkg.go.dev/github.com/crossplane/upjet/v2/pkg/resource/json) | v2.5.1 | 1,702 | shared family: Not run. pkg/resource/json in v2.5.1 defines TFParser/JSParser as jsoniter.Config values over github.com/json-iterator/go, the already selected json-iterator parser; no own JSON parsing. |
| [github.com/Jeffail/gabs/v2](https://pkg.go.dev/github.com/Jeffail/gabs/v2) | v2.7.0 | 517 | shared family: Not run. gabs.go in v2.7.0 parses with encoding/json (json.Unmarshal in ParseJSON, json.NewDecoder in ParseJSONDecoder/ParseJSONBuffer); it is a container wrapper with no own JSON parser. |
| [github.com/go-json-experiment/json](https://pkg.go.dev/github.com/go-json-experiment/json) | v1.27.2 | 516 | unresolved shared family: Not run. The pinned v1.27.2 module is the experimental upstream of Go's encoding/json/v2 and jsontext: jsontext/decode.go has 1,220 lines in both it and Go 1.27.1 src/encoding/json/jsontext/decode.go with 8 differing diff lines, and arshal_any.go differs by 14 diff lines of 289. Go 1.27.1 encoding/json delegates to that v2 code, so this path would share the parser of the separately inventoried standard API. |
| [github.com/elastic/go-structform/json](https://pkg.go.dev/github.com/elastic/go-structform/json) | v0.0.12 | 372 | unresolved: Own hand-written state-machine parser (json/parse.go: Parse([]byte, structform.Visitor), ParseReader, Parser.stepValue/stepDict/stepArray) that reports values to a caller Visitor. Not run: below go-faster/jx (451) and the cell reached its ten-path ceiling. |
| [github.com/francoispqt/gojay](https://pkg.go.dev/github.com/francoispqt/gojay) | v1.2.13 | 357 | unresolved: Own decoder, but only through caller-implemented UnmarshalerJSONObject/UnmarshalerJSONArray types for a known schema. Its untyped Decoder.Interface/DecodeInterface path (decode_interface.go) finds the value bounds and then calls encoding/json.Unmarshal, so a generic untyped harness would test encoding/json. Not run. |

Queries: `json`, `json parser`, `json decoder`, `json unmarshal`, `json iterator`; limit 100 each; 500 hits, 474 unique.
