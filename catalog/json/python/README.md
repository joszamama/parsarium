# JSON / Python — pilot

**Status:** pilot_two_verified_bounded_search_pending; incomplete. 2 verified third-party paths, 1 verified standard APIs, 2 verified Docker harnesses.

This is a two-parser pilot, not a completed popularity search or top-ten claim. Nine named package leads were inspected via PyPI/project documentation; the bounded PyPI Simple Index name search remains pending. Seven leads have no pinned control result. Pydantic is verified on its documented byte API with Rust LLVM coverage and input-dependent AFL++ feedback from its pinned Jiter 0.18.0 parser; its package downloads include use unrelated to JSON. The standalone jiter lead shares that underlying parser family and remains unverified as a separate API. The Python standard path explicitly selects the pure-Python json decoder/scanner; CPython default _json accelerator is not covered or ranked. Two valid controls establish their tested subset only.

[Ranking and search limits](../../../data/python/json/ranking.md) · [Standard API inventory](../../../data/python/json/standard.json)

## Third-party parsers

- [pydantic](pydantic/README.md) — verified Docker harness
- [simplejson](simplejson/README.md) — verified Docker harness

## Standard and runtime APIs

- [json.load(BytesIO(local UTF-8 bytes), cls=PurePythonJSONDecoder)](standard/json-load-bytesio-local-utf-8-bytes-cls-purepythonjsondecoder/README.md) — verified Docker harness
