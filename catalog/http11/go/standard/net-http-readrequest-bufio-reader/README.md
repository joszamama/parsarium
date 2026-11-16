# net/http.ReadRequest(*bufio.Reader) — HTTP/1.1 / Go

- **Runtime:** Go 1.27.1 linux/arm64 standard library
- **Input API:** `net/http.ReadRequest(*bufio.Reader)`
- **Official documentation:** [reference](https://pkg.go.dev/net/http@go1.27.1)
- **Valid control:** [`controls/http11/request.http`](../../../../../controls/http11/request.http)
- **Inventory and verification:** [standard API record](../../../../../data/go/http11/standard.json) · [saved result](../../../../../data/go/http11/verification.json)

## Observed control result

```json
{
  "host": "example.test",
  "method": "GET",
  "proto": "HTTP/1.1",
  "target": "/parsarium?x=1"
}
```

[Control adapter](../../../../../adapters/go/http11_std.go)

## Run this target

```sh
python3 parsarium.py build http11 go stdlib_request
python3 parsarium.py run http11 go stdlib_request controls/http11/request.http
```
