# @sylphx/gust-core — HTTP/1.1 / JavaScript

Pinned release: `0.1.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/sylphx-gust-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript sylphx_gust_core
python3 parsarium.py run http11 javascript sylphx_gust_core controls/http11/request.http
python3 parsarium.py replay http11 javascript sylphx_gust_core CORPUS_DIR runs/http11-sylphx_gust_core-replay
python3 parsarium.py afl build http11 javascript sylphx_gust_core
python3 parsarium.py afl prepare http11 javascript sylphx_gust_core runs/http11-sylphx_gust_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
