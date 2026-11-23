# Small valid HTTP/1.1 responses for Parsarium's http11 targets that are
# verified on a response control (controls/http11/response*.http).
# Every response has an HTTP/1.1 status line, CRLF-terminated header lines and
# an empty CRLF line. A response with content is framed either by a matching
# Content-Length or by chunked transfer coding (never both, RFC 9112 6.2-6.3);
# 204 and 304 responses carry no content and no framing field. Header values
# hold no quote or backslash.

<start> ::= <length_response> | <chunked_response> | <bodyless_response>

<length_response> ::= "HTTP/1.1 " <status_with_content> "\r\n" <optional_headers> <content_type>? <length_framed>
<chunked_response> ::= "HTTP/1.1 " <status_with_content> "\r\n" <optional_headers> <content_type>? <chunked_framed>
<bodyless_response> ::= "HTTP/1.1 " <status_without_content> "\r\n" <optional_headers> "\r\n"

# status-line = HTTP-version SP status-code SP [ reason-phrase ]
<status_with_content> ::= "200 OK" | "200 " | "200 Fine" | "201 Created" | "202 Accepted" \
                        | "203 Non-Authoritative Information" | "301 Moved Permanently" \
                        | "302 Found" | "400 Bad Request" | "403 Forbidden" | "404 Not Found" \
                        | "500 Internal Server Error" | "503 Service Unavailable"
<status_without_content> ::= "204 No Content" | "304 Not Modified"

# Fixed order, each at most once, so no field name repeats.
<optional_headers> ::= <date>? <server>? <cache_control>? <x_parsarium>? <connection>?
<date> ::= "Date:" <ows> ("Sun, 22 Nov 2026 10:00:00 GMT" | "Mon, 23 Nov 2026 08:30:15 GMT") "\r\n"
<server> ::= "Server:" <ows> "parsarium-fandango/1\r\n"
<cache_control> ::= "Cache-Control:" <ows> ("no-cache" | "max-age=60") "\r\n"
<x_parsarium> ::= "X-Parsarium:" <ows> "yes\r\n"
<connection> ::= "Connection:" <ows> ("close" | "keep-alive") "\r\n"

<content_type> ::= ("Content-Type" | "content-type") ":" <ows> <media_type> "\r\n"
<media_type> ::= "text/plain" | "text/plain; charset=utf-8" | "text/html" | "application/json"

# The length field is the last field, so its value and the content agree.
<length_framed> ::= ("Content-Length" | "content-length") ":" <ows> <sized_content>
<sized_content> ::= "9\r\n\r\nparsarium" | "2\r\n\r\nOK" | "3\r\n\r\nx=1" | "0\r\n\r\n" \
                  | "11\r\n\r\nhello world" | "11\r\n\r\n{\"ok\":true}" \
                  | "18\r\n\r\nline one\nline two\n"

# chunked-body = *chunk last-chunk trailer-section CRLF
<chunked_framed> ::= "Transfer-Encoding:" <ows> "chunked\r\n\r\n" <chunk>{0,3} "0\r\n" <trailer_section> "\r\n"
<chunk> ::= "9\r\nparsarium\r\n" | "2\r\nOK\r\n" | "3\r\nx=1\r\n" | "b\r\nhello world\r\n" \
          | "B\r\nhello world\r\n" | "009\r\nparsarium\r\n" | "9;ext=1\r\nparsarium\r\n" \
          | "12\r\nline one\nline two\n\r\n"
<trailer_section> ::= "" | "X-Trailer:" <ows> "done\r\n"

<ows> ::= " " | ""
