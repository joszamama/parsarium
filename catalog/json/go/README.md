# JSON / Go — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 1 verified standard APIs, 5 verified Docker harnesses.

Five Go JSON paths passed two valid structure-aware controls, source-scoped coverage and stable AFL++ feedback: json-iterator/go (18,454 Imported by), tidwall/gjson (10,420), ugorji/go/codec (10,142), goccy/go-json (4,192), and buger/jsonparser (2,171). GJSON and buger/jsonparser are path-query parsers, and their adapter traverses every value in the controls; buger/jsonparser is not claimed to validate an arbitrary complete JSON document. go-codec is multi-format: its Imported by count measures the package across several formats, not JSON-specific use. sonic (2,428) and three other numeric leads remain unverified, so the fifth path is not a definitive fifth most-used parser. Search is bounded to five pkg.go.dev queries of 100 results each. The Go standard encoding/json path is separate and unranked. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/go/json/ranking.md) · [Standard API inventory](../../../data/go/json/standard.json)

## Third-party parsers

- [github.com/json-iterator/go](github-com-json-iterator-go/README.md) — verified Docker harness
- [github.com/tidwall/gjson](github-com-tidwall-gjson/README.md) — verified Docker harness
- [github.com/ugorji/go/codec](github-com-ugorji-go-codec/README.md) — verified Docker harness
- [github.com/goccy/go-json](github-com-goccy-go-json/README.md) — verified Docker harness
- [github.com/buger/jsonparser](github-com-buger-jsonparser/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/json.Unmarshal(\[\]byte, any)](standard/encoding-json-unmarshal-byte-any/README.md) — verified Docker harness
