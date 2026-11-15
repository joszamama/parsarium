"""Parse one HTTP/1.1 request from bytes using h11."""

import h11


def parse_http11(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    connection = h11.Connection(h11.SERVER)
    connection.receive_data(data)
    request = connection.next_event()
    if not isinstance(request, h11.Request) or request.http_version != b"1.1":
        return None
    headers = dict(request.headers)
    result = {"method": request.method.decode("latin1"),
              "target": request.target.decode("latin1"),
              "host": headers[b"host"].decode("latin1")}
    while True:
        event = connection.next_event()
        if event is h11.NEED_DATA or event is h11.PAUSED:
            return None
        if isinstance(event, h11.EndOfMessage):
            break
    return result


def fuzz_one_input(data: bytes):
    try:
        parse_http11(data)
    except h11.RemoteProtocolError:
        pass
