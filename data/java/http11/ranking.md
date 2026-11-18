# JAVA × HTTP/1.1: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev version-level directDependentCount.

| Rank | Package | Release | Direct dependents (deps.dev) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [commons-httpclient](https://hc.apache.org/httpclient-legacy/apidocs/org/apache/commons/httpclient/HttpParser.html) | 3.1 | 1,484 | HTTP/1.1 response status line and headers from local stream | Apache Commons HttpClient 3.x native HTTP response-head parser |
| 2 | [httpcore](https://hc.apache.org/httpcomponents-core-4.4.x/current/httpcore/apidocs/org/apache/http/impl/io/DefaultHttpRequestParser.html) | 4.4.16 | 1,414 | HTTP/1.1 request line and headers from local stream | Apache HttpComponents Core HTTP/1.1 parser, 4.x branch; shared upstream with httpcore5 |
| 3 | [httpcore5](https://hc.apache.org/httpcomponents-core-5.4.x/5.4.4/httpcore5/apidocs/org/apache/hc/core5/http/impl/io/DefaultHttpRequestParser.html) | 5.4.4 | 532 | HTTP/1.1 request line and headers from local stream | Apache HttpComponents Core HTTP/1.1 parser, 5.x branch |
| 4 | [netty](https://netty.io/3.10/api/org/jboss/netty/handler/codec/http/HttpRequestDecoder.html) | 3.10.6.Final | 213 | HTTP/1.1 request line and headers from local bytes | Netty 3 HTTP request decoder; prior major branch of netty-codec-http |
| 5 | [httpcore-nio](https://hc.apache.org/httpcomponents-core-4.4.x/current/httpcore-nio/apidocs/org/apache/http/nio/NHttpMessageParser.html) | 4.4.16 | 64 | HTTP/1.1 request line and headers from local channel | Apache HttpComponents Core 4.x NIO request parser |
| 6 | [nanohttpd](https://javadoc.io/static/org.nanohttpd/nanohttpd/2.3.1/fi/iki/elonen/NanoHTTPD.HTTPSession.html) | 2.3.1 | 54 | HTTP/1.1 request method, target, Host and X-Parsarium headers from local stream; protocol version is internal and not reported | NanoHTTPD native HTTP request parser |
| 7 | [jodd-http](https://http.jodd.org/connection) | 6.3.0 | 39 | HTTP/1.1 request line and headers from local stream | Jodd HTTP native request parser |
| 8 | [netty-codec-http](https://netty.io/4.2/api/io/netty/handler/codec/http/HttpRequestDecoder.html) | 4.2.20.Final | 23 | HTTP/1.1 request line and headers from local bytes | Netty 4 HTTP request decoder |
| 9 | [netty5-codec-http](https://github.com/netty/netty/blob/netty-5.0.0.Alpha5/codec-http/src/main/java/io/netty5/handler/codec/http/HttpRequestDecoder.java) | 5.0.0.Alpha5 | 15 | HTTP/1.1 request line and headers from local bytes | Netty 5 HTTP request decoder, alpha branch; shares project ancestry with Netty 3 and 4 |
| 10 | [grizzly-http](https://github.com/eclipse-ee4j/glassfish-grizzly/blob/5.0.3/modules/http/src/main/java/org/glassfish/grizzly/http/HttpServerFilter.java) | 5.0.3 | 8 | HTTP/1.1 request line and headers from local bytes | Grizzly native HTTP server codec |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
