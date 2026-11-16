# net/http.ReadResponse(*bufio.Reader, *Request) — HTTP/1.1 / Go

- **Runtime:** Go 1.27.1 linux/arm64 standard library
- **Input API:** `net/http.ReadResponse(*bufio.Reader, *Request)`
- **Official documentation:** [reference](https://pkg.go.dev/net/http@go1.27.1)
- **Valid control:** [`controls/http11/response.http`](../../../../../controls/http11/response.http)
- **Inventory and verification:** [standard API record](../../../../../data/go/http11/standard.json) · [saved result](../../../../../data/go/http11/verification.json)

## Observed control result

```json
{
  "body": "parsarium",
  "proto": "HTTP/1.1",
  "status": 200
}
```

[Control adapter](../../../../../adapters/go/http11_std.go)

## Run this target

```sh
python3 parsarium.py build http11 go stdlib_response
python3 parsarium.py run http11 go stdlib_response controls/http11/response.http
```
