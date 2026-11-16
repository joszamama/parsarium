"""Exercise CPython 3.13.1 http.client.parse_headers on local HTTP bytes."""
import adapter
import http.client

def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    return adapter.parse('http.client.parse_headers', data)

def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError, http.client.HTTPException):
        pass
