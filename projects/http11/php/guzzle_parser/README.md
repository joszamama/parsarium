# guzzle/parser — HTTP/1.1 / PHP

Pinned release: `v3.9.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/php/guzzle-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 php guzzle_parser
python3 parsarium.py run http11 php guzzle_parser controls/http11/request.http
python3 parsarium.py replay http11 php guzzle_parser CORPUS_DIR runs/http11-guzzle_parser-replay
python3 parsarium.py afl build http11 php guzzle_parser
python3 parsarium.py afl prepare http11 php guzzle_parser runs/http11-guzzle_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
