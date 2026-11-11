"""Generate valid HTTP/1.1 request and response wire controls."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
request = (
    b"GET /parsarium?x=1 HTTP/1.1\r\n"
    b"Host: example.test\r\n"
    b"X-Parsarium: yes\r\n"
    b"Connection: close\r\n"
    b"\r\n"
)
body = b"parsarium"
response = (
    b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
    + f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    + body
)
(ROOT / "request.http").write_bytes(request)
(ROOT / "response.http").write_bytes(response)
print(f"Wrote {len(request)} request bytes and {len(response)} response bytes")
