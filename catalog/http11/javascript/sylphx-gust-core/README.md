# @sylphx/gust-core — HTTP/1.1 / JavaScript

- **Pinned release:** `0.1.9`
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** gust-core WASM
- **Local input API:** `initWasm(); WasmCore.parse_http(Uint8Array)`
- **Documentation:** [API reference](<https://unpkg.com/@sylphx/gust-core@0.1.9/dist/index.d.ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/javascript/sylphx_gust_core/README.md)

```sh
python3 parsarium.py build http11 javascript sylphx_gust_core
python3 parsarium.py run http11 javascript sylphx_gust_core controls/http11/request.http
```
