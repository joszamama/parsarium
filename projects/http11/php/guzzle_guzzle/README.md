# guzzle/guzzle — HTTP/1.1 / PHP

Pinned release: `v3.9.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/php/guzzle-guzzle/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 php guzzle_guzzle
python3 parsarium.py run http11 php guzzle_guzzle controls/http11/request.http
python3 parsarium.py replay http11 php guzzle_guzzle CORPUS_DIR runs/http11-guzzle_guzzle-replay
python3 parsarium.py afl build http11 php guzzle_guzzle
python3 parsarium.py afl prepare http11 php guzzle_guzzle runs/http11-guzzle_guzzle-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
