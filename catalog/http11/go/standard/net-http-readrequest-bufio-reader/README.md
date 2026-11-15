# net/http.ReadRequest(*bufio.Reader) — HTTP/1.1 / Go

- **Runtime:** Go 1.27.1 darwin/arm64 standard library
- **Input API:** `net/http.ReadRequest(*bufio.Reader)`
- **Official documentation:** [reference](https://pkg.go.dev/net/http@go1.27.1)
- **Valid control:** [`controls/http11/request.http`](../../../../../controls/http11/request.http)
- **Inventory and verification:** [standard API record](../../../../../data/go/http11/standard.json) · [saved result](../../../../../data/go/http11/verification.json)

## Observed control result

GET /parsarium?x=1, Host example.test, HTTP/1.1

[Control adapter](../../../../../adapters/go/http11_std.go)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
