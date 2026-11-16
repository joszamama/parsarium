# github.com/cloudwego/hertz/pkg/protocol/http1/req — HTTP/1.1 / Go

Pinned release: `v0.10.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-cloudwego-hertz-pkg-protocol-http1-req/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_cloudwego_hertz_pkg_protocol_http1_req
python3 parsarium.py run http11 go github_com_cloudwego_hertz_pkg_protocol_http1_req controls/http11/request.http
python3 parsarium.py replay http11 go github_com_cloudwego_hertz_pkg_protocol_http1_req CORPUS_DIR runs/http11-github_com_cloudwego_hertz_pkg_protocol_http1_req-replay
python3 parsarium.py afl build http11 go github_com_cloudwego_hertz_pkg_protocol_http1_req
python3 parsarium.py afl prepare http11 go github_com_cloudwego_hertz_pkg_protocol_http1_req runs/http11-github_com_cloudwego_hertz_pkg_protocol_http1_req-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
