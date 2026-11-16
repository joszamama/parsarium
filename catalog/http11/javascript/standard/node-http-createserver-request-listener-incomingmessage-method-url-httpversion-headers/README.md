# node:http.createServer request listener; IncomingMessage.method/url/httpVersion/headers — HTTP/1.1 / JavaScript

- **Runtime:** Node.js 26.10.0
- **Input API:** `node:http.createServer request listener; IncomingMessage.method/url/httpVersion/headers`
- **Official documentation:** [reference](https://nodejs.org/download/release/v26.10.0/docs/api/http.html)
- **Valid control:** [`controls/http11/request.http`](../../../../../controls/http11/request.http)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/http11/standard.json) · [saved result](../../../../../data/javascript/http11/verification.json)

**Parser family:** Node.js bundled HTTP parser

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

[Control adapter](../../../../../adapters/javascript/http11_node.mjs)

## Run this target

```sh
python3 parsarium.py build http11 javascript stdlib_node_http
python3 parsarium.py run http11 javascript stdlib_node_http controls/http11/request.http
```
