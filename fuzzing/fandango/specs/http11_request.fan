# Small valid HTTP/1.1 requests for Parsarium's http11 cell.
# Every request has an origin-form start line, a Host header, CRLF-terminated
# header lines and an empty CRLF line. POST bodies carry a matching
# Content-Length; other methods carry no body.

<start> ::= <bodyless_request> | <post_request>

<bodyless_request> ::= <bodyless_method> " " <target> " HTTP/1.1\r\n" <host> <optional_headers> "\r\n"
<post_request> ::= "POST " <target> " HTTP/1.1\r\n" <host> <optional_headers> <content_type> <framed_body>

<bodyless_method> ::= "GET" | "HEAD" | "OPTIONS" | "DELETE"

<target> ::= "/" | "/parsarium" | "/parsarium?x=1" | "/a/b?x=1&y=2" | "/index.html"

<host> ::= "Host:" <ows> <host_value> "\r\n"
<host_value> ::= "example.test" | "example.test:8080" | "localhost"

# Fixed order, each at most once, so no header name repeats.
<optional_headers> ::= <user_agent>? <accept>? <x_parsarium>? <connection>?
<user_agent> ::= "User-Agent:" <ows> "parsarium-fandango/1\r\n"
<accept> ::= "Accept:" <ows> ("*/*" | "text/plain") "\r\n"
<x_parsarium> ::= "X-Parsarium:" <ows> "yes\r\n"
<connection> ::= "Connection:" <ows> ("close" | "keep-alive") "\r\n"

<content_type> ::= "Content-Type:" <ows> ("text/plain" | "application/x-www-form-urlencoded") "\r\n"
<framed_body> ::= "Content-Length:" <ows> "9\r\n\r\nparsarium" \
                | "Content-Length:" <ows> "3\r\n\r\nx=1" \
                | "Content-Length:" <ows> "0\r\n\r\n"

<ows> ::= " " | ""
