# phpstandard/raw-request-factory — HTTP/1.1 / PHP

Pinned release: `1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/php/phpstandard-raw-request-factory/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 php phpstandard_raw_request_factory
python3 parsarium.py run http11 php phpstandard_raw_request_factory controls/http11/request.http
python3 parsarium.py replay http11 php phpstandard_raw_request_factory CORPUS_DIR runs/http11-phpstandard_raw_request_factory-replay
python3 parsarium.py afl build http11 php phpstandard_raw_request_factory
python3 parsarium.py afl prepare http11 php phpstandard_raw_request_factory runs/http11-phpstandard_raw_request_factory-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
