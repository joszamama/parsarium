# nanohttpd — HTTP/1.1 / Java

- **Pinned release:** `2.3.1`
- **Upstream:** [source repository](<https://github.com/NanoHttpd/nanohttpd>) · [Maven Central](<https://central.sonatype.com/artifact/org.nanohttpd/nanohttpd>)
- **License:** BSD-3-Clause
- **Parsed scope:** HTTP/1.1 request method, target, Host and X-Parsarium headers from local stream; protocol version is internal and not reported
- **Underlying family:** NanoHTTPD native HTTP request parser
- **Local input API:** `NanoHTTPD.HTTPSession(TempFileManager, local InputStream, OutputStream).execute(); override serve(IHTTPSession) to inspect parsed method, URI, query and headers`
- **Documentation:** [API reference](<https://javadoc.io/static/org.nanohttpd/nanohttpd/2.3.1/fi/iki/elonen/NanoHTTPD.HTTPSession.html>)
- **Catalog evidence:** [parser record](../../../../data/java/http11/parsers.json) · [control verification](../../../../data/java/http11/verification.json) · [within-ecosystem ranking](../../../../data/java/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "host": "example.test",
  "x_parsarium": "yes"
}
```

A protected HTTPSession is instantiated inside a NanoHTTPD subclass using local byte streams; execute() invokes serve() with parsed request fields. The control includes Connection: close, so the normal session shutdown SocketException is caught after a parsed callback. No listening socket is opened.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/java/nanohttpd/README.md)

```sh
python3 parsarium.py build http11 java nanohttpd
python3 parsarium.py run http11 java nanohttpd controls/http11/request.http
```
