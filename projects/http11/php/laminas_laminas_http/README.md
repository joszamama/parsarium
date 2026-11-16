# laminas/laminas-http — HTTP/1.1 / PHP

Pinned release: `2.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/php/laminas-laminas-http/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 php laminas_laminas_http
python3 parsarium.py run http11 php laminas_laminas_http controls/http11/request.http
python3 parsarium.py replay http11 php laminas_laminas_http CORPUS_DIR runs/http11-laminas_laminas_http-replay
python3 parsarium.py afl build http11 php laminas_laminas_http
python3 parsarium.py afl prepare http11 php laminas_laminas_http runs/http11-laminas_laminas_http-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
