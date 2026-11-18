# proxy.py — HTTP/1.1 / Python

- **Pinned release:** `2.4.10`
- **Upstream:** [source repository](<https://github.com/abhinavsingh/proxy.py>) · [PyPI](<https://pypi.org/project/proxy.py/>)
- **License:** BSD-3-Clause
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** proxy.py Python HTTP parser
- **Local input API:** `proxy.http.parser.HttpParser.request(bytes)`
- **Documentation:** [API reference](<https://proxypy.readthedocs.io/en/latest/pkg/proxy.http.parser/>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "host": "example.test"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/python/proxy_py/README.md)

```sh
python3 parsarium.py build http11 python proxy_py
python3 parsarium.py run http11 python proxy_py controls/http11/request.http
```
