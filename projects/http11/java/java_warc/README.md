# java-warc — HTTP/1.1 / Java

Pinned release: `1.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/java-warc/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java java_warc
python3 parsarium.py run http11 java java_warc controls/http11/response.http
python3 parsarium.py replay http11 java java_warc CORPUS_DIR runs/http11-java_warc-replay
python3 parsarium.py afl build http11 java java_warc
python3 parsarium.py afl prepare http11 java java_warc runs/http11-java_warc-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
