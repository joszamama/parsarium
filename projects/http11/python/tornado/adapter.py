"""Run one pinned Python HTTP/1.1 parser against a local valid control."""

import asyncio
import json
import socket
import sys
from pathlib import Path


def decoded(value):
    return value.decode("latin-1") if isinstance(value, bytes) else str(value)


def request_result(method, target, host):
    return {"method": decoded(method), "target": decoded(target), "host": decoded(host)}


def parse(name, raw):
    text = raw.decode("latin-1")

    if name in ("h11", "h11-mypyc", "h11pro"):
        import importlib

        module = importlib.import_module({"h11": "h11", "h11-mypyc": "h11_mypyc",
                                          "h11pro": "h11pro"}[name])
        connection = module.Connection(module.SERVER)
        connection.receive_data(raw)
        event = connection.next_event()
        return request_result(event.method, event.target, dict(event.headers)[b"host"])

    if name == "httptools":
        import httptools

        class Callbacks:
            def __init__(self):
                self.target = None
                self.headers = {}

            def on_url(self, target):
                self.target = target

            def on_header(self, key, value):
                self.headers[key.lower()] = value

        callbacks = Callbacks()
        parser = httptools.HttpRequestParser(callbacks)
        parser.feed_data(raw)
        return request_result(parser.get_method(), callbacks.target,
                              callbacks.headers[b"host"])

    if name == "zttp":
        import zttp

        connection = zttp.Connection(zttp.SERVER)
        connection.receive_data(raw)
        event = connection.next_event()
        headers = {key.lower(): value for key, value in event.headers}
        return request_result(event.method, event.target, headers[b"host"])

    if name == "h11r":
        import h11r

        connection = h11r.Connection(h11r.Role.SERVER)
        connection.receive_data(raw)
        event = connection.next_event()
        headers = {key.lower(): value for key, value in event.headers}
        return request_result(event.method, event.target, headers[b"host"])

    if name == "httppackets":
        from io import BytesIO
        from httppackets.http_1_1_parser import Decision, parse_http_1_1_requests

        result = {}

        def on_headers(method, target, headers):
            result.update(request_result(method, target, headers["host"][0]))
            return Decision.READ_BODY

        parse_http_1_1_requests(BytesIO(raw), on_headers=on_headers,
                               on_body=lambda reader: reader.read())
        return result

    if name == "http-parse":
        from http_parse import parse as parse_request

        result = parse_request(text)
        return request_result(result.method, result.path, result.headers["Host"])

    if name == "http-pyparser":
        from http_pyparser import HTTPParser

        result = HTTPParser().parser(text)
        return request_result(result.method, result.real_path, result.host)

    if name == "httparse":
        from httparse import RequestParser

        result = RequestParser().parse(raw)
        headers = {header.name.lower(): header.value for header in result.headers}
        return request_result(result.method, result.path, headers["host"])

    if name == "pycohttpparser":
        from pycohttpparser.api import Parser

        result = Parser().parse_request(memoryview(raw))
        headers = {bytes(key).lower(): bytes(value) for key, value in result.headers}
        return request_result(bytes(result.method), bytes(result.path), headers[b"host"])

    if name == "parse-http-header-line":
        from parse_http_header_line import parse_name_value

        key, value = parse_name_value(text.split("\r\n")[1])
        return {"header": key, "value": value}

    if name == "ParseRawHTTP":
        from ParseRawHTTP import ParseRawHTTP

        url, method, headers, _ = ParseRawHTTP(text)
        return request_result(method, "/" + url.split("/", 1)[1], headers["Host"])

    if name == "tp-http-request-response-parser":
        from TP_HTTP_Request_Response_Parser import TP_HTTP_REQUEST_PARSER

        result = TP_HTTP_REQUEST_PARSER(text)
        return {"method": result.request_method, "version": result.request_httpVersion}

    if name == "gunicorn-h1c":
        from gunicorn_h1c import parse_request

        result = parse_request(raw)
        return request_result(result["method"], result["path"],
                              dict(result["headers"])[b"Host"])

    if name == "h1parser":
        from h1parser import ParseHeader

        result = ParseHeader(raw)
        if not result.is_valid_request:
            raise ValueError("request header did not parse")
        return request_result(bytes(result.headers[b"_method"]),
                              bytes(result.headers[b"_url"]),
                              bytes(result.headers[b"host"]))

    if name == "parserheader":
        from parserheader import parserheader

        result = parserheader(text)
        return {"host": result["Host"], "x_parsarium": result["X-Parsarium"]}

    if name == "websockets":
        from io import BytesIO
        from websockets.http11 import Request

        stream = BytesIO(raw)

        def read_line(limit, _error):
            if False:
                yield None
            return stream.readline(limit)

        parser = Request.parse(read_line)
        try:
            while True:
                next(parser)
        except StopIteration as finished:
            request = finished.value
        return {"target": request.path, "host": request.headers["Host"]}

    if name == "proxy.py":
        from proxy.http.parser import HttpParser

        result = HttpParser.request(raw)
        return request_result(result.method, result.path, result.headers[b"host"][1])

    if name == "http-parser":
        from http_parser.parser import HttpParser

        parser = HttpParser()
        consumed = parser.execute(raw, len(raw))
        if consumed != len(raw) or not parser.is_headers_complete():
            raise ValueError("incomplete HTTP request")
        return request_result(parser.get_method(), parser.get_url(),
                              parser.get_headers()["Host"])

    if name == "tornado":
        from tornado.http1connection import HTTP1Connection
        from tornado.httputil import HTTPMessageDelegate
        from tornado.iostream import IOStream

        class Delegate(HTTPMessageDelegate):
            body = b""
            finished = False

            def headers_received(self, start_line, headers):
                self.start_line = start_line
                self.headers = headers

            def data_received(self, chunk):
                self.body += chunk

            def finish(self):
                self.finished = True

        async def run():
            receiver, sender = socket.socketpair()
            receiver.setblocking(False)
            sender.sendall(raw)
            sender.shutdown(socket.SHUT_WR)
            stream = IOStream(receiver)
            delegate = Delegate()
            try:
                await asyncio.wait_for(HTTP1Connection(stream, is_client=True)
                                       .read_response(delegate), 3)
                if not delegate.finished:
                    raise ValueError("response not finished")
                return {"status": delegate.start_line.code,
                        "content_type": delegate.headers["Content-Type"],
                        "body": delegate.body.decode("ascii")}
            finally:
                stream.close()
                sender.close()

        return asyncio.run(run())

    if name == "Twisted":
        from twisted.internet.testing import StringTransport
        from twisted.web.http import HTTPChannel, Request

        class ObservedRequest(Request):
            parsed = None

            def process(self):
                type(self).parsed = request_result(self.method, self.uri,
                                                   self.getHeader("host"))
                self.finish()

        class Factory:
            def log(self, _request):
                pass

        channel = HTTPChannel()
        channel.factory = Factory()
        channel.requestFactory = ObservedRequest
        channel.makeConnection(StringTransport())
        channel.dataReceived(raw)
        if ObservedRequest.parsed is None:
            raise ValueError("request not processed")
        return ObservedRequest.parsed

    raise ValueError(f"unknown parser: {name}")


if __name__ == "__main__":
    print(json.dumps(parse(sys.argv[1], Path(sys.argv[2]).read_bytes()), sort_keys=True))
