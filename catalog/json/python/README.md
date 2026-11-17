# JSON / Python — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 1 verified standard APIs, 3 verified Docker harnesses.

Three positive-signal Python JSON third-party paths pass valid nested object and array controls with source-level parser coverage and AFL++ feedback: pydantic 2.14.3 (1,139,429,690 PyPI Stats last-month downloads), orjson 3.13.0 (218,014,317), and simplejson 4.3.0 (49,365,386). orjson shares the yyjson C syntax-parser family, but this pilot measures its Rust deserializer traversal and not the C source lines. PyPI package downloads include encoding use and dependencies. Six targeted documented leads remain unverified; bounded PyPI Simple Index search has not yet been run. Python standard json is separately verified.

[Ranking and search limits](../../../data/python/json/ranking.md) · [Standard API inventory](../../../data/python/json/standard.json)

## Third-party parsers

- [pydantic](pydantic/README.md) — verified Docker harness
- [orjson](orjson/README.md) — verified Docker harness
- [simplejson](simplejson/README.md) — verified Docker harness

## Standard and runtime APIs

- [json.load(BytesIO(local UTF-8 bytes), cls=PurePythonJSONDecoder)](standard/json-load-bytesio-local-utf-8-bytes-cls-purepythonjsondecoder/README.md) — verified Docker harness
