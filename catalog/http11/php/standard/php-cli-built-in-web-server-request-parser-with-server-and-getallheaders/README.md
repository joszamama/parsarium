# PHP CLI built-in web server request parser with $_SERVER and getallheaders — HTTP/1.1 / PHP

- **Runtime:** PHP 8.5.12 CLI built-in web server
- **Input API:** `Built-in server accepts local HTTP/1.1 bytes over a loopback TCP stream; router receives parsed request fields in $_SERVER and getallheaders()`
- **Official documentation:** [reference](https://www.php.net/manual/en/features.commandline.webserver.php) · [reference](https://www.php.net/manual/en/reserved.variables.server.php) · [reference](https://www.php.net/manual/en/function.getallheaders.php)
- **Valid control:** [`controls/http11/request.http`](../../../../../controls/http11/request.http)
- **Inventory and verification:** [standard API record](../../../../../data/php/http11/standard.json) · [saved result](../../../../../data/php/http11/verification.json)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "version": "1.1",
  "host": "example.test",
  "custom": "yes"
}
```

[Control adapter](../../../../../adapters/php/http11/runtime_router.php)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
