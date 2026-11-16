# github.com/meta-apex/metarpc/codec/http — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20250816075809-78e603aff299`
- **License:** Apache-2.0
- **Parsed scope:** request message
- **Underlying family:** fasthttp-derived metarpc parser
- **Local input API:** `Parser.Parse([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/meta-apex/metarpc/codec/http@v0.0.0-20250816075809-78e603aff299>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "host": "example.test"
}
```

This package shares a parser family or code lineage with another row; package paths do not imply independent engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_meta_apex_metarpc_codec_http/README.md)

```sh
python3 parsarium.py build http11 go github_com_meta_apex_metarpc_codec_http
python3 parsarium.py run http11 go github_com_meta_apex_metarpc_codec_http controls/http11/request.http
```
