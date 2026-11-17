# C × JSON: selected parsers (pilot)

Three verified third-party paths. The target is up to ten; the other leads stay unselected until they pass the same gates.

## Adoption metric

Debian popcon `sourcemax` installations by source package, captured 2026-11-17 from [the pinned snapshot](registry-snapshot.json) (source Last-Modified 2026-11-16). These are Debian package installations, often transitive dependencies, and miss vendored copies. The counts compare only C JSON candidates and do not establish JSON-specific use.

| Rank | Package | Release | Installations | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [jansson](https://jansson.readthedocs.io/en/latest/apiref.html#c.json_loadb) | 2.15.1 | 282,984 | Own recursive-descent `src/load.c` |
| 2 | [json-c](https://json-c.github.io/json-c/json-c-0.19/doc/html/json__tokener_8h.html) | 0.19 | 269,736 | Own incremental `json_tokener.c` |
| 3 | [cJSON](https://github.com/DaveGamble/cJSON/blob/v1.7.19/README.md) | 1.7.19 | 150,958 | Own recursive-descent `cJSON.c` |

cJSON uses its documented `cJSON_ParseWithLengthOpts` local byte-buffer API. The [pinned source archive](https://github.com/DaveGamble/cJSON/releases/tag/v1.7.19) has SHA-256 `7fa616e3046edfa7a28a32d5f9eacfd23f92900fe1f8ccd988c1662f30454562` and an MIT LICENSE. Its Docker control traverses the parsed cJSON tree and compares the full nested JSON value to the valid object control. Two repeated valid controls produce identical parser-source LLVM regions and AFL++ bitmaps; the valid nested-array control changes 39 parser features and 29 AFL tuples ([receipt](afl-feedback.json)).

[Parser records](parsers.json) · [control results](verification.json) · [standard inventory](standard.json). ISO C documents no JSON parser API.

## Unresolved leads

| Lead | Conan recipe | Popcon installations | Status |
| --- | --- | ---: | --- |
| [yyjson](https://github.com/ibireme/yyjson) | yes | 14,868 | Documented byte API; control and feedback not run |
| [jsmn](https://github.com/zserge/jsmn) | yes | 11 | Tokenizer-only lead; below the stated supplemental adoption threshold |
| [parson](https://github.com/kgabis/parson) | yes | unavailable | No comparable Debian source count; input API requires a NUL-terminated string |

Conan Center search: recipe-name substring `json` (24 hits) plus `jansson`, `jsmn`, `parson` targeted names (3 hits), at most 100 results per query; 27 recorded hits, 27 unique. Other Conan hits include C++ libraries, validators and jsonnet. The release source and valid controls support only the observed JSON subset; a complete RFC 8259 implementation claim would need more evidence.
