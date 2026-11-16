# http.client.HTTPConnection.getresponse — HTTP/1.1 / Python

- **Runtime:** CPython 3.13.1 standard library
- **Input API:** `http.client.HTTPConnection.request() and getresponse() over a local socket`
- **Official documentation:** [reference](https://docs.python.org/3.13/library/http.client.html#http.client.HTTPConnection.getresponse)
- **Valid control:** [`controls/http11/response.http`](../../../../../controls/http11/response.http)
- **Inventory and verification:** [standard API record](../../../../../data/python/http11/standard.json) · [saved result](../../../../../data/python/http11/verification.json)

## Observed control result

```json
{
  "status": 200,
  "content_type": "text/plain",
  "body": "parsarium"
}
```

[Control adapter](../../../../../adapters/python/http11/standard.py)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
