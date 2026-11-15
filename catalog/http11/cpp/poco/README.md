# poco — HTTP/1.1 / C++

- **Pinned release:** `1.15.4`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
