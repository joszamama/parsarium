# facil-legacy — HTTP/1.1 / C

Pinned release: `0.7.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/facil-legacy/README.md)

The pinned Docker control parsed a complete GET request, including its path, query, version, and Host header. LLVM coverage reached 144 lines in facil.io's `http1_parser.h`; AFL++ produced 78 feedback edges.

The harness copies each input into a writable buffer of exactly its length and calls facil.io's documented `http1_parse` once. It reports the method, path, query, version and Host header when one complete request uses every byte. facil.io 0.7 and C STL 0.8 belong to the same parser family.

## Run from the repository root

```sh
python3 parsarium.py build http11 c facil-legacy
python3 parsarium.py run http11 c facil-legacy controls/http11/request.http
python3 parsarium.py replay http11 c facil-legacy CORPUS_DIR runs/http11-facil-legacy-replay
python3 parsarium.py afl build http11 c facil-legacy
python3 parsarium.py afl prepare http11 c facil-legacy runs/http11-facil-legacy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
