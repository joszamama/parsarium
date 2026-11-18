# libmicrohttpd — HTTP/1.1 / C

- **Pinned release:** `1.0.10`
- **Upstream:** [Debian](<https://tracker.debian.org/pkg/libmicrohttpd>)
- **License:** LGPL-2.1-or-later
- **Parsed scope:** HTTP/1.1 GET request method, path, query argument and version from local socket stream
- **Underlying family:** GNU libmicrohttpd HTTP/1 request parser in an embedded C server, separate from llhttp and PicoHTTPParser
- **Local input API:** `MHD_start_daemon(MHD_USE_NO_LISTEN_SOCKET | MHD_USE_INTERNAL_POLLING_THREAD, ...); MHD_add_connection(daemon, local socketpair stream, ...); access handler receives parsed method, URL, version and MHD_lookup_connection_value returns parsed query`
- **Documentation:** [API reference](<https://www.gnu.org/software/libmicrohttpd/manual/libmicrohttpd.pdf>)
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

[Docker harness and verification receipt](../../../../projects/http11/c/libmicrohttpd/README.md)

```sh
python3 parsarium.py build http11 c libmicrohttpd
python3 parsarium.py run http11 c libmicrohttpd controls/http11/request.http
```
