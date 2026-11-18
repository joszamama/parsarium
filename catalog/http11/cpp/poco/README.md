# poco — HTTP/1.1 / C++

- **Pinned release:** `1.15.4`
- **Upstream:** [source repository](<https://github.com/pocoproject/poco>) · [Debian](<https://tracker.debian.org/pkg/poco>)
- **License:** BSL-1.0
- **Parsed scope:** HTTP/1.1 request method, URI, version, and Host header
- **Underlying family:** Poco.Net HTTPRequest parser
- **Local input API:** `Poco::Net::HTTPRequest::read(std::istream&) on a local std::ifstream`
- **Documentation:** [API reference](<https://docs.pocoproject.org/current/Poco.Net.HTTPRequest.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/http11/parsers.json) · [control verification](../../../../data/cpp/http11/verification.json) · [within-ecosystem ranking](../../../../data/cpp/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "1.1",
  "host": "example.test"
}
```

Native C++ HTTP request reader in Poco.Net; distinct from Boost.Beast.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/cpp/poco/README.md)

```sh
python3 parsarium.py build http11 cpp poco
python3 parsarium.py run http11 cpp poco controls/http11/request.http
```
