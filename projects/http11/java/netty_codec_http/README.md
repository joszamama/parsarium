# netty-codec-http — HTTP/1.1 / Java

Pinned release: `4.2.20.Final`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/netty-codec-http/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java netty_codec_http
python3 parsarium.py run http11 java netty_codec_http controls/http11/request.http
python3 parsarium.py replay http11 java netty_codec_http CORPUS_DIR runs/http11-netty_codec_http-replay
python3 parsarium.py afl build http11 java netty_codec_http
python3 parsarium.py afl prepare http11 java netty_codec_http runs/http11-netty_codec_http-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
