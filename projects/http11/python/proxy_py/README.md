# proxy.py — HTTP/1.1 / Python

Pinned release: `2.4.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/proxy-py/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python proxy_py
python3 parsarium.py run http11 python proxy_py controls/http11/request.http
python3 parsarium.py replay http11 python proxy_py CORPUS_DIR runs/http11-proxy_py-replay
python3 parsarium.py afl build http11 python proxy_py
python3 parsarium.py afl prepare http11 python proxy_py runs/http11-proxy_py-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
