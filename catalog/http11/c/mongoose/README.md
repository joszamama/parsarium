# mongoose — HTTP/1.1 / C

- **Pinned release:** `7.23`
- **Upstream:** [source repository](<https://github.com/cesanta/mongoose>) · [Debian](<https://tracker.debian.org/pkg/mongoose>)
- **License:** GPL-2.0-only
- **Parsed scope:** HTTP/1.1 GET request method, target, query and version
- **Underlying family:** Mongoose C HTTP request parser; related to CivetWeb and LibHTTP ancestry
- **Local input API:** `mg_http_parse(const char *local request bytes, size_t len, struct mg_http_message *out)`
- **Documentation:** [API reference](<https://mongoose.ws/docs/api/http/#mg_http_parse>)
- **Catalog evidence:** [parser record](../../../../data/c/http11/parsers.json) · [control verification](../../../../data/c/http11/verification.json) · [within-ecosystem ranking](../../../../data/c/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "1.1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/c/mongoose/README.md)

```sh
python3 parsarium.py build http11 c mongoose
python3 parsarium.py run http11 c mongoose controls/http11/request.http
```
