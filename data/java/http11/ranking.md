# Java × HTTP/1.1: verified parser ranking

5 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T12:42:21.756954+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [httpcore](https://hc.apache.org/httpcomponents-core-4.4.x/current/httpcore/apidocs/org/apache/http/impl/io/DefaultHttpRequestParser.html) | org.apache.httpcomponents:httpcore:4.4.16 | 1,414 | HTTP/1.1 request line and headers from local stream | Apache HttpComponents Core HTTP/1.1 parser, 4.x branch; shared upstream with httpcore5 |
| 2 | [httpcore5](https://hc.apache.org/httpcomponents-core-5.4.x/5.4.4/httpcore5/apidocs/org/apache/hc/core5/http/impl/io/DefaultHttpRequestParser.html) | org.apache.httpcomponents.core5:httpcore5:5.4.4 | 532 | HTTP/1.1 request line and headers from local stream | Apache HttpComponents Core HTTP/1.1 parser, 5.x branch |
| 3 | [netty-codec-http](https://netty.io/4.2/api/io/netty/handler/codec/http/HttpRequestDecoder.html) | io.netty:netty-codec-http:4.2.20.Final | 23 | HTTP/1.1 request line and headers from local bytes | Netty 4 HTTP request decoder |
| 4 | [jetty-http](https://javadoc.jetty.org/jetty-12.1/org/eclipse/jetty/http/HttpTester.html) | org.eclipse.jetty:jetty-http:12.1.15 | 4 | HTTP/1.1 request line and headers from local bytes | Jetty HTTP/1.1 HttpParser |
| 5 | [http1_1-parser](https://github.com/deanhiller/webpieces/blob/master/http/http1_1-parser/src/main/java/org/webpieces/httpparser/api/HttpParser.java) | org.webpieces.http:http1_1-parser:2.1.109 | 3 | HTTP/1.1 request line and headers from local bytes | WebPieces HTTP/1.1 parser |
