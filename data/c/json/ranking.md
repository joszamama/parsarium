# C × JSON: selected parsers (pilot)

Five verified third-party paths, ranked by one Debian metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Debian popcon `sourcemax` installations by source package, captured 2026-11-17 from the pinned snapshot [`popcon-sourcemax-by_inst.gz`](../../curation/popcon-sourcemax-by_inst.gz) (SHA-256 `9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8`, source Last-Modified 2026-11-16). These are Debian package installations, often transitive dependencies, and miss vendored copies. The counts compare only C JSON candidates and do not establish JSON-specific use.

| Rank | Package | Release | Debian source | Installations | Parser family |
| ---: | --- | --- | --- | ---: | --- |
| 1 | [jansson](https://jansson.readthedocs.io/en/latest/apiref.html#c.json_loadb) | 2.15.1 | `jansson` | 282,984 | Own recursive-descent `src/load.c` |
| 2 | [json-c](https://json-c.github.io/json-c/json-c-0.19/doc/html/json__tokener_8h.html) | 0.19 | `json-c` | 269,736 | Own incremental `json_tokener.c` |
| 3 | [JSON-GLib](https://gnome.pages.gitlab.gnome.org/json-glib/method.Parser.load_from_data.html) | 1.10.8 | `json-glib` | 163,249 | Own JsonParser over own `json-scanner.c` |
| 4 | [cJSON](https://github.com/DaveGamble/cJSON/blob/v1.7.19/README.md) | 1.7.19 | `cjson` | 150,958 | Own recursive-descent `cJSON.c` |
| 5 | [yyjson](https://github.com/ibireme/yyjson/blob/0.13.0/doc/API.md) | 0.13.0 | `yyjson` | 14,868 | Own native reader in `src/yyjson.c` |

cJSON uses its documented `cJSON_ParseWithLengthOpts` local byte-buffer API. The [pinned source archive](https://github.com/DaveGamble/cJSON/releases/tag/v1.7.19) has SHA-256 `7fa616e3046edfa7a28a32d5f9eacfd23f92900fe1f8ccd988c1662f30454562` and an MIT LICENSE. Its Docker control traverses the parsed cJSON tree and compares the full nested JSON value to the valid object control. Two repeated valid controls produce identical parser-source LLVM regions and AFL++ bitmaps; the valid nested-array control changes 39 parser features and 29 AFL tuples ([receipt](afl-feedback.json)).

yyjson uses the documented `yyjson_read(dat, len, 0)` byte-buffer API. The [pinned release](https://github.com/ibireme/yyjson/releases/tag/0.13.0) source archive has SHA-256 `34e0f62a2bc11ab20d601e8ca1cc2b2079503aa45119a19133d89d19b94a0fae` and an MIT LICENSE. Its full parsed document matches each valid control; repeat feedback is stable, and the second control changes 473 parser regions and 408 AFL tuples.

JSON-GLib 1.10.8 comes from the [GNOME release tarball](https://download.gnome.org/sources/json-glib/1.10/json-glib-1.10.8.tar.xz), SHA-256 `55c5c141a564245b8f8fbe7698663c87a45a7333c2a2c56f06f811ab73b212dd` (LGPL-2.1-or-later), the same upstream version as Debian forky/sid. The harness calls the [documented](https://gnome.pages.gitlab.gnome.org/json-glib/method.Parser.load_from_data.html) `json_parser_load_from_data` with the exact byte length after `json_parser_set_strict(parser, TRUE)`. `json-parser.c` is JSON-GLib's own recursive-descent parser over its own `json-scanner.c` tokenizer; GLib provides only containers. Each valid control's JsonNode tree equals Python's `json.loads` result, including member order and int64/double kinds. The base control covers 1,176 JSON-GLib lines (438 in `json-parser.c`). The parser-only AFL++ probe instruments only the parser, scanner and node/object/array/value sources (checked with `nm`); three runs per control repeat exactly and the controls differ by 22 of 304/298 tuples and 34 source lines ([receipt](../../../fuzzing/afl-native/json/c/json-glib/differential.json)).

[Parser records](parsers.json) · [control results](verification.json) · [standard inventory](standard.json). ISO C documents no JSON parser API.

## Unresolved leads

| Lead | Popcon installations | Status |
| --- | ---: | --- |
| [jq](https://github.com/jqlang/jq/releases/tag/jq-1.8.2) | 141,218 | Not control-tested |
| [libfastjson](https://download.rsyslog.com/libfastjson/libfastjson-1.2609.0.tar.gz) | 91,226 | Not control-tested |
| [json-parser](https://github.com/json-parser/json-parser/releases/tag/v1.1.0) | 844 | Not control-tested |
| [parson](https://github.com/kgabis/parson) | unavailable | Verified technically; no Debian source package |
| [frozen](https://github.com/cesanta/frozen) | 16 | Fails the nested-object control |
| [jsmn](https://github.com/zserge/jsmn) | 11 | Tokenizer only; not eligible for the value gate |
| [liblaxjson](https://github.com/andrewrk/liblaxjson) | 1 | Not control-tested |

frozen 1.7's `json_walk` types tokens but leaves values as raw spans; its `json_unescape` turns the control's `\u00e9` into the single byte 0xE9 rather than UTF-8, so the nested-object control cannot match. jsmn reports only object/array/string/primitive token spans without decoding strings or typing primitives, so the harness would have to interpret JSON itself. parson 1.5.4 passed both controls, 530 own lines and 34 stable AFL++ tuple differences in candidate commit 271447a6, but has no Debian source package and so no primary value; stars are not an allowed fallback outside PLY cells.

## Search

Conan Center search: recipe-name substring `json` (24 hits) plus `jansson`, `jsmn`, `parson` targeted names (3 hits), at most 100 results per query; 27 recorded hits, 27 unique. That surface missed Debian-packaged C parsers, so the same hashed popcon snapshot was searched on 2026-11-17 for Debian source names containing `json`: 320 hits, 320 unique, all recorded and classified in the [snapshot](registry-snapshot.json). C JSON parser libraries among them are json-c, JSON-GLib, cJSON, libfastjson, yyjson, libjsonparser and liblaxjson; jsonrpc-glib, lua-cjson, tree-sitter-json, wal2json, lz4json and gjh-asl-json are C code but not separate JSON value libraries, and the rest are other languages, tools or C++ (picojson belongs to the C++ cell). Exact source-name lookups in the same file add jansson, jq (141,218), frozen (16) and jsmn (11); parson has no Debian source. The pinned releases and valid controls support only the observed JSON subset; a complete RFC 8259 implementation claim would need more evidence.
