# C × JSON: selected parsers (pilot)

2 control-verified third-party paths selected. The ceiling is ten; this pilot builds the two highest-adoption C JSON parser leads and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Debian popcon sourcemax installations by source package, captured 2026-11-17 from `https://popcon.debian.org/sourcemax/by_inst.gz` (Last-Modified 2026-11-16; [snapshot](registry-snapshot.json)). Candidates come from the Conan Center recipe tree.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jansson](https://jansson.readthedocs.io/en/latest/apiref.html#c.json_loadb) | 2.15.1 | 282,984 | RFC 8259 JSON text (object or array root) into a json_t tree | jansson recursive-descent decoder (src/load.c) |
| 2 | [json-c](https://json-c.github.io/json-c/json-c-0.19/doc/html/json__tokener_8h.html) | 0.19 | 269,736 | RFC 8259 JSON text (object or array root, strict mode, trailing whitespace only) into a json_object tree | json-c incremental state-machine tokener (json_tokener.c) |

Input API: `json_loadb(const char *buffer, size_t buflen, size_t flags, json_error_t *error)` with flags 0, documented in the release tarball's `doc/apiref.rst`; the harness fixes `json_object_seed(1)` so object hashing repeats. Source: [release tarball](https://github.com/akheron/jansson/releases/download/v2.15.1/jansson-2.15.1.tar.gz), SHA-256 `0c7114dc0b2d22a670724a1f95922029d7077c19dbf79a584cb8084d2f267f2f`.

json-c input API: `json_tokener_parse_ex(tok, str, len)` with `JSON_TOKENER_STRICT`, documented in the release tarball's `json_tokener.h`. The harness copies the bytes, passes the final `'\0'` in `len` as the header requires at end of input, and rejects anything after the value other than JSON whitespace. It selects `JSON_C_STR_HASH_PERLLIKE` so object hashing has no random seed. Source: [release tarball](https://github.com/json-c/json-c/releases/download/json-c-0.19-20260627/json-c-0.19.tar.gz), SHA-256 `37ad0249902e301bd9052bf712e511fcc6acff4ecaad4b5900aad9ce564e26de`.

The two are separate code bases. The jansson/json-c gap (13,248 installs, under 5%) is too small to read as a preference.

## Standard API (unranked)

None. The ISO C standard library (WG14 N3220) documents no JSON parser; see [standard.json](standard.json).

## Lead log

Numeric leads from the same snapshot, not verified and not selected.

| Lead | Conan recipe | Popcon installed | Status |
| --- | --- | ---: | --- |
| [cJSON](https://github.com/DaveGamble/cJSON) | yes | 150,958 | cJSON_ParseWithLength(value, length); most of its count is in popcon's no-files column. Not built. |
| [yyjson](https://github.com/ibireme/yyjson) | yes | 14,868 | yyjson_read(dat, len, flg) over bytes. Not built. |
| [jsmn](https://github.com/zserge/jsmn) | yes | 11 | Tokenizer only; no value tree. Not built. |
| [parson](https://github.com/kgabis/parson) | yes | — | No Debian source package, so no comparable count; json_parse_string needs a NUL-terminated string. Not built. |

Excluded Conan hits: 18 C++ libraries (for example nlohmann_json, rapidjson, simdjson, jsoncpp, cpp-yyjson), two schema validators, and jsonnet.

Queries: recipe-name substring `json` (24 hits) plus targeted names `jansson`, `jsmn`, `parson` (3 hits); limit 100 each; 27 hits, 27 unique. Popcon counts Debian installations, mostly as dependencies, and misses vendored copies; it is a package-level signal, not JSON-specific use.
