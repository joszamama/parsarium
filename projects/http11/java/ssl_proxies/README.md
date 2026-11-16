# ssl-proxies — HTTP/1.1 / Java

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/ssl-proxies/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java ssl_proxies
python3 parsarium.py run http11 java ssl_proxies controls/http11/response.http
python3 parsarium.py replay http11 java ssl_proxies CORPUS_DIR runs/http11-ssl_proxies-replay
python3 parsarium.py afl build http11 java ssl_proxies
python3 parsarium.py afl prepare http11 java ssl_proxies runs/http11-ssl_proxies-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
