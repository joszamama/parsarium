# JSON / Python — pilot

**Status:** pilot_six_selected_search_bounded; incomplete. 6 verified third-party paths, 1 verified standard APIs, 6 verified Docker harnesses.

Six positive-signal Python JSON third-party paths pass valid nested object and array controls with source-level parser coverage and AFL++ feedback: pydantic 2.14.3 (1,139,429,690 PyPI Stats last-month downloads), orjson 3.13.0 (218,014,317), simplejson 4.3.0 (49,365,386), ijson 3.6.0 (46,615,664), msgspec 0.22.0 (39,138,375), and ujson 6.1.0 (29,543,889). Pydantic embeds Jiter; orjson shares the yyjson C syntax-parser family but this pilot measures its Rust deserializer, not vendored C source lines. ijson uses the asserted yajl2_c backend, with pinned YAJL C tokenizer and Python extension coverage; its source-built embedded YAJL -O0 route differs from the official Linux wheel linkage and optimisation, and its other backends are untested. msgspec uses its own C JSON decoder in _core.c through untyped msgspec.json.decode; its source-built clang -O0 path differs from the official GCC wheel, typed decoding is untested, and JSON decoder sections are counted separately from other codecs in the same file. ujson uses its own UltraJSON C decoder with vendored double-conversion C++ for fractional numbers; both controls equal an exact CPython json oracle tree, and duplicate-key and edge-number behavior is recorded from source, not tested. PyPI package downloads include non-parse uses and transitive installs. Three targeted documented leads remain unverified; bounded PyPI Simple Index search has not yet been run. Python standard json is separately verified.

[Ranking and search limits](../../../data/python/json/ranking.md) · [Standard API inventory](../../../data/python/json/standard.json)

## Third-party parsers

- [pydantic](pydantic/README.md) — verified Docker harness
- [orjson](orjson/README.md) — verified Docker harness
- [simplejson](simplejson/README.md) — verified Docker harness
- [ijson](ijson/README.md) — verified Docker harness
- [msgspec](msgspec/README.md) — verified Docker harness
- [ujson](ujson/README.md) — verified Docker harness

## Standard and runtime APIs

- [json.load(BytesIO(local UTF-8 bytes), cls=PurePythonJSONDecoder)](standard/json-load-bytesio-local-utf-8-bytes-cls-purepythonjsondecoder/README.md) — verified Docker harness
