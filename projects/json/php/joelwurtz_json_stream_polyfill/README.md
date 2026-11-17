# joelwurtz/json-stream-polyfill — JSON / PHP

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/joelwurtz-json-stream-polyfill/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php joelwurtz_json_stream_polyfill
python3 parsarium.py run json php joelwurtz_json_stream_polyfill controls/json/nested-object.json
python3 parsarium.py replay json php joelwurtz_json_stream_polyfill CORPUS_DIR runs/json-joelwurtz_json_stream_polyfill-replay
python3 parsarium.py afl build json php joelwurtz_json_stream_polyfill
python3 parsarium.py afl prepare json php joelwurtz_json_stream_polyfill runs/json-joelwurtz_json_stream_polyfill-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
