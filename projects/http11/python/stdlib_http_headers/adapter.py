"""Verify CPython 3.13 HTTP/1.1 runtime APIs with local wire controls."""

import http.client
import http.server
import io
import json
import socket
import sys
from pathlib import Path


def parse(api, raw):
    if api == "http.client.HTTPConnection.getresponse":
        receiver, sender = socket.socketpair()
        sender.sendall(raw)
        sender.shutdown(socket.SHUT_WR)

        class LocalConnection(http.client.HTTPConnection):
            def connect(self):
                self.sock = receiver

        connection = LocalConnection("example.test")
        try:
            connection.request("GET", "/parsarium")
            response = connection.getresponse()
            return {"status": response.status,
                    "content_type": response.getheader("Content-Type"),
                    "body": response.read().decode("ascii")}
        finally:
            connection.close()
            sender.close()

    if api == "http.server.BaseHTTPRequestHandler":
        class Handler(http.server.BaseHTTPRequestHandler):
            parsed = None

            def do_GET(self):
                type(self).parsed = {"method": self.command, "target": self.path,
                                     "host": self.headers["Host"]}

            def log_message(self, *_args):
                pass

        class Server:
            server_name = "localhost"
            server_port = 0

        receiver, sender = socket.socketpair()
        try:
            sender.sendall(raw)
            sender.shutdown(socket.SHUT_WR)
            Handler(receiver, ("localhost", 0), Server())
            if Handler.parsed is None:
                raise ValueError("request did not parse")
            return Handler.parsed
        finally:
            receiver.close()
            sender.close()

    if api == "http.client.parse_headers":
        fields = raw.split(b"\r\n", 1)[1]
        headers = http.client.parse_headers(io.BytesIO(fields))
        # A field the message does not carry is omitted.
        result = {}
        if headers["Content-Type"] is not None:
            result["content_type"] = headers["Content-Type"]
        if headers["Content-Length"] is not None:
            result["content_length"] = int(headers["Content-Length"])
        return result

    raise ValueError(api)


if __name__ == "__main__":
    print(json.dumps(parse(sys.argv[1], Path(sys.argv[2]).read_bytes()), sort_keys=True))
