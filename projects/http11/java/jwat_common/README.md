# jwat-common — HTTP/1.1 / Java

Pinned release: `1.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/jwat-common/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java jwat_common
python3 parsarium.py run http11 java jwat_common controls/http11/request.http
python3 parsarium.py replay http11 java jwat_common CORPUS_DIR runs/http11-jwat_common-replay
python3 parsarium.py afl build http11 java jwat_common
python3 parsarium.py afl prepare http11 java jwat_common runs/http11-jwat_common-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
