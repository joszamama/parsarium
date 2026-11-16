# jetty-http — HTTP/1.1 / Java

Pinned release: `12.1.15`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/jetty-http/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java jetty_http
python3 parsarium.py run http11 java jetty_http controls/http11/request.http
python3 parsarium.py replay http11 java jetty_http CORPUS_DIR runs/http11-jetty_http-replay
python3 parsarium.py afl build http11 java jetty_http
python3 parsarium.py afl prepare http11 java jetty_http runs/http11-jetty_http-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
