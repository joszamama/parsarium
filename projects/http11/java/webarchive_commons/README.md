# webarchive-commons — HTTP/1.1 / Java

Pinned release: `3.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/webarchive-commons/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java webarchive_commons
python3 parsarium.py run http11 java webarchive_commons controls/http11/request.http
python3 parsarium.py replay http11 java webarchive_commons CORPUS_DIR runs/http11-webarchive_commons-replay
python3 parsarium.py afl build http11 java webarchive_commons
python3 parsarium.py afl prepare http11 java webarchive_commons runs/http11-webarchive_commons-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
