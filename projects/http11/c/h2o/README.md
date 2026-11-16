# h2o — HTTP/1.1 / C

Pinned release: `2.2.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/h2o/README.md)

H2O 2.2.6 bundles PicoHTTPParser in `deps/picohttpparser`. This C harness calls that bundled `phr_parse_request` copy, so it shares its parser family with [picohttpparser](../picohttpparser/README.md) and the [C++ h2o path](../../cpp/h2o/README.md); it is not an independent HTTP engine.

The harness accepts up to 1 MiB per request and reserves 32 header slots. It retains the parsed method and target as slices of the input buffer until the result is printed.

The pinned Docker control parsed `GET /parsarium?x=1 HTTP/1.1`, covered 126 lines in H2O's bundled PicoHTTPParser, and produced 94 AFL++ feedback edges.

## Run from the repository root

```sh
python3 parsarium.py build http11 c h2o
python3 parsarium.py run http11 c h2o controls/http11/request.http
python3 parsarium.py replay http11 c h2o CORPUS_DIR runs/http11-h2o-replay
python3 parsarium.py afl build http11 c h2o
python3 parsarium.py afl prepare http11 c h2o runs/http11-h2o-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
