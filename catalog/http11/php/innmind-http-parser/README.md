# innmind/http-parser — HTTP/1.1 / PHP

- **Pinned release:** `4.0.0`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Innmind HTTP stream parser
- **Local input API:** `Request\Parse::default(Clock::live())(local request byte stream); method, target, version, and headers`
- **Documentation:** [API reference](<https://github.com/Innmind/http-parser/blob/d937a6173daa7bfce121452f35ccafc723859b73/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/http11/parsers.json) · [control verification](../../../../data/php/http11/verification.json) · [within-ecosystem ranking](../../../../data/php/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

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

Native request frame parser over Innmind IO; pinned version 4.0.0 requires PHP 8.4, replayed with Homebrew PHP 8.4.27.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/innmind_http_parser/README.md)

```sh
python3 parsarium.py build http11 php innmind_http_parser
python3 parsarium.py run http11 php innmind_http_parser controls/http11/request.http
```
