"""Parse HTTP/1.1 request bytes with http-parser's native HttpParser."""

from http_parser.parser import HttpParser


def decoded(value):
    return value.decode("latin-1") if isinstance(value, bytes) else str(value)


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    parser = HttpParser()
    consumed = parser.execute(data, len(data))
    if consumed != len(data) or not parser.is_headers_complete():
        return None
    headers = {decoded(key).lower(): decoded(value)
               for key, value in parser.get_headers().items()}
    if "host" not in headers:
        return None
    return {"method": decoded(parser.get_method()),
            "target": decoded(parser.get_url()), "host": headers["host"]}


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError, KeyError):
        pass
