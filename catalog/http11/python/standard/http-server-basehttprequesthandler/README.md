# http.server.BaseHTTPRequestHandler — HTTP/1.1 / Python

- **Runtime:** CPython 3.13.1 standard library
- **Input API:** `http.server.BaseHTTPRequestHandler(local socket, client address, server) parses and dispatches request`
- **Official documentation:** [reference](https://docs.python.org/3.13/library/http.server.html#http.server.BaseHTTPRequestHandler)
- **Valid control:** [`controls/http11/request.http`](../../../../../controls/http11/request.http)
- **Inventory and verification:** [standard API record](../../../../../data/python/http11/standard.json) · [saved result](../../../../../data/python/http11/verification.json)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "host": "example.test"
}
```

[Control adapter](../../../../../adapters/python/http11/standard.py)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
