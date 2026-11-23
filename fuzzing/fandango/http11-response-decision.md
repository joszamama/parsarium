# HTTP/1.1 response spec

Ten `http11` targets are verified on a response control, not a request, so
the request grammar [`http11_request.fan`](specs/http11_request.fan) gives
them nothing to parse:

| Target | Control |
| --- | --- |
| `c/serf`, `cpp/serf` | `controls/http11/response_serf.http` |
| `go/stdlib_response`, `java/commons_httpclient`, `javascript/parse_raw_http`, `python/stdlib_http_headers`, `python/stdlib_http_response`, `python/tornado`, `rust/async_h1`, `rust/minihttpse` | `controls/http11/response.http` |

On the 50-file request corpus (`--seed 2027`), nine of them rejected every
file at the status line, and `python/stdlib_http_headers` read only the
header fields. Fanbase has no HTTP spec.

`parsarium fandango generate http11 ECO SLUG` now picks the spec from the
target's manifest: a control under `controls/http11/response` selects the
local [`http11_response.fan`](specs/http11_response.fan); every other target
keeps `http11_request.fan`. `--spec` still overrides both.

## Grammar

One response per file, always `HTTP/1.1`, CRLF line endings:

- a status code with content (200, 201, 202, 203, 301, 302, 400, 403, 404,
  500, 503) and its reason phrase, an empty reason (`200 `) or a different
  one (`200 Fine`); or 204 or 304, which carry no content and no framing field;
- optional `Date`, `Server`, `Cache-Control`, `X-Parsarium` and `Connection`,
  each at most once and in that order, then an optional `Content-Type` (or
  `content-type`) with one of four media types;
- content framed by exactly one of a `Content-Length` (or `content-length`)
  that matches 0, 2, 3, 9, 11 or 18 bytes, or `Transfer-Encoding: chunked`
  with zero to three chunks, hex sizes in lower or upper case or with leading
  zeros, an optional `;ext=1` chunk extension, and an optional `X-Trailer`
  trailer field;
- no space, or one space, after each field colon.

No 1xx responses, close-delimited content, content codings, repeated fields,
obsolete line folding or quotes and backslashes in field values.

## Check

[`controls/http11/check_responses.py`](../../controls/http11/check_responses.py)
reads each file twice: with h11 0.16.0 as a client that sent `GET`, and with
its own RFC 9112 walk (status line, token field names, field values, exactly
one framing for statuses with content, chunk sizes and trailers, every byte
consumed). The two must agree on status and content.

```sh
PYTHONHASHSEED=0 .venv/fandango-1.3.1-locked/bin/fandango fuzz \
  -f fuzzing/fandango/specs/http11_response.fan -n 200 --random-seed 1 \
  --progress-bar off -d /tmp/fandango-http11-response -x .http
docker run --rm -v "$PWD:/r:ro" -v /tmp/fandango-http11-response:/in:ro python:3.13-slim \
  sh -c 'pip install -q h11==0.16.0 && python3 -I /r/controls/http11/check_responses.py /in'
```

On 2026-11-23 this produced 200 distinct files of 29 to 235 bytes: 82 framed
by `Content-Length`, 76 chunked (21 with a chunk extension, 34 with a
trailer) and 42 204 or 304 responses; 74 carry a `Content-Type`. h11, the
walk and `fandango parse --file-mode binary` accepted all 200. The 50 files
from `parsarium fandango generate http11 go stdlib_response … --count 50
--seed 2027` (17 length-framed, 14 chunked, 19 without content) passed the
same check, as did both response controls, and a second run reproduced them
byte for byte.

185 of the 200 files have at least one field with no space after the colon,
which RFC 9112 allows (`OWS` is optional); the request grammar does the same.
`javascript/parse_raw_http` requires `": "` and rejects those files.
