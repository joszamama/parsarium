# commons-httpclient — HTTP/1.1 / Java

Pinned release: `3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/commons-httpclient/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java commons_httpclient
python3 parsarium.py run http11 java commons_httpclient controls/http11/response.http
python3 parsarium.py replay http11 java commons_httpclient CORPUS_DIR runs/http11-commons_httpclient-replay
python3 parsarium.py afl build http11 java commons_httpclient
python3 parsarium.py afl prepare http11 java commons_httpclient runs/http11-commons_httpclient-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
