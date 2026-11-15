# net/http.ReadResponse(*bufio.Reader, *Request) — HTTP/1.1 / Go

- **Runtime:** Go 1.27.1 darwin/arm64 standard library
- **Input API:** `net/http.ReadResponse(*bufio.Reader, *Request)`
- **Official documentation:** [reference](https://pkg.go.dev/net/http@go1.27.1)
- **Valid control:** [`controls/http11/response.http`](../../../../../controls/http11/response.http)
- **Inventory and verification:** [standard API record](../../../../../data/go/http11/standard.json) · [saved result](../../../../../data/go/http11/verification.json)

## Observed control result

HTTP/1.1 200 OK, body parsarium

[Control adapter](../../../../../adapters/go/http11_std.go)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
