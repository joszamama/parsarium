# zttp — HTTP/1.1 / Python

- **Pinned release:** `0.0.35`
- **License:** BSD-3-Clause
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** zttp Zig parser
- **Local input API:** `zttp.Connection(zttp.SERVER).receive_data(bytes); next_event()`
- **Documentation:** [API reference](<https://pypi.org/project/zttp/0.0.35/>)
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

[Docker harness and verification receipt](../../../../projects/http11/python/zttp/README.md)

```sh
python3 parsarium.py build http11 python zttp
python3 parsarium.py run http11 python zttp controls/http11/request.http
```
