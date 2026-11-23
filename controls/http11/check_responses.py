"""Check HTTP/1.1 response files with h11 and a separate RFC 9112 framing walk.

Each *.http file in the given directories must be one complete response: a
status line, unique token-named fields, and content framed by exactly one of
Content-Length or chunked coding (none for 1xx, 204 and 304). h11 0.16.0, as
a client that sent a GET, must read the same status and content as the walk,
and the walk must consume every byte. Run it where h11 is installed, for example:

    docker run --rm -v "$PWD:/r:ro" python:3.13-slim sh -c \
      'pip install -q h11==0.16.0 && python3 -I /r/controls/http11/check_responses.py DIR'
"""
import json
import re
import sys
from pathlib import Path

import h11

TOKEN = re.compile(rb"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")
FIELD_VALUE = re.compile(rb"[\x21-\x7e]([\x20-\x7e\t]*[\x21-\x7e])?|")
STATUS = re.compile(rb"HTTP/1\.1 ([1-5][0-9][0-9]) ([\t\x20-\x7e]*)")


def own_walk(raw: bytes) -> dict:
    head, sep, rest = raw.partition(b"\r\n\r\n")
    assert sep, "no empty line"
    lines = head.split(b"\r\n")
    m = STATUS.fullmatch(lines[0])
    assert m, f"bad status line {lines[0]!r}"
    status = int(m.group(1))
    fields = []
    for line in lines[1:]:
        name, colon, value = line.partition(b":")
        assert colon and TOKEN.fullmatch(name), f"bad field {line!r}"
        value = value.strip(b" \t")
        assert FIELD_VALUE.fullmatch(value), f"bad value {line!r}"
        fields.append((name.lower(), value))
    names = [n for n, _ in fields]
    assert len(names) == len(set(names)), "repeated field"
    d = dict(fields)
    assert not (b"content-length" in d and b"transfer-encoding" in d), "both framings"
    if status in (204, 304) or status < 200:
        assert b"content-length" not in d and b"transfer-encoding" not in d
        assert rest == b"", "content after bodyless response"
        return {"status": status, "body": b""}
    if b"content-length" in d:
        n = int(d[b"content-length"])
        assert len(rest) == n, f"content length {n} != {len(rest)}"
        return {"status": status, "body": rest}
    assert d.get(b"transfer-encoding") == b"chunked", "no framing"
    body, pos = b"", 0
    while True:
        end = rest.index(b"\r\n", pos)
        size_text = rest[pos:end].split(b";", 1)[0]
        assert re.fullmatch(rb"[0-9A-Fa-f]+", size_text), f"bad chunk size {size_text!r}"
        size = int(size_text, 16)
        pos = end + 2
        if size == 0:
            break
        body += rest[pos:pos + size]
        assert rest[pos + size:pos + size + 2] == b"\r\n", "chunk not CRLF-terminated"
        pos += size + 2
    while True:
        end = rest.index(b"\r\n", pos)
        line = rest[pos:end]
        pos = end + 2
        if not line:
            break
        name, colon, _ = line.partition(b":")
        assert colon and TOKEN.fullmatch(name), f"bad trailer {line!r}"
    assert pos == len(rest), "bytes after chunked body"
    return {"status": status, "body": body}


def with_h11(raw: bytes) -> dict:
    conn = h11.Connection(our_role=h11.CLIENT)
    conn.send(h11.Request(method="GET", target="/", headers=[("Host", "example.test")]))
    conn.send(h11.EndOfMessage())
    conn.receive_data(raw)
    conn.receive_data(b"")
    status, body = None, b""
    while True:
        event = conn.next_event()
        if isinstance(event, h11.Response):
            status = event.status_code
        elif isinstance(event, h11.Data):
            body += bytes(event.data)
        elif isinstance(event, h11.EndOfMessage):
            break
        elif event is h11.NEED_DATA:
            raise AssertionError("h11 needs more data")
        elif isinstance(event, h11.InformationalResponse):
            raise AssertionError("informational response")
    return {"status": status, "body": body}


def main() -> int:
    failures = 0
    summary = {"files": 0, "ok": 0}
    for path in sorted(p for d in sys.argv[1:] for p in Path(d).glob("*.http")):
        raw = path.read_bytes()
        summary["files"] += 1
        try:
            a, b = own_walk(raw), with_h11(raw)
            assert a == b, f"walk {a} != h11 {b}"
            summary["ok"] += 1
        except Exception as error:  # report every failure
            failures += 1
            print(f"FAIL {path.name}: {type(error).__name__}: {error}")
    summary["h11"] = h11.__version__
    print(json.dumps(summary))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
