# JSON / C — pilot

**Status:** pilot_eight_selected_search_bounded; incomplete. 8 verified third-party paths, 0 verified standard APIs, 8 verified Docker harnesses.

Eight C JSON third-party paths pass two valid controls with format-aware tree results, parser source coverage and stable AFL++ feedback. The original Conan recipe search missed Debian-packaged C parsers; a bounded Debian source-name search for 'json' (320 hits) plus exact lookups for jansson, jq, frozen, jsmn and parson in the same hashed popcon snapshot found the Debian-packaged C parser leads. libfastjson is a json-c fork and shares the json-c tokener family; jq's count is the jq source package (mostly the command-line program), and its jv C API is documented on the project wiki without a stability commitment; jq numbers have one kind, so integer/float in its tree comes from the preserved decimal literal. frozen fails the nested-object control (\u00e9 decoded to one Latin-1 byte), jsmn is tokenizer-only, and liblaxjson (1 installation) and parson (no Debian source) remain unselected. Debian installations mostly reflect dependencies and miss vendored copies. These paths do not establish a definitive top ten or full RFC 8259 compliance. ISO C documents no JSON API.

[Ranking and search limits](../../../data/c/json/ranking.md) · [Standard API inventory](../../../data/c/json/standard.json)

## Third-party parsers

- [jansson](jansson/README.md) — verified Docker harness
- [json-c](json-c/README.md) — verified Docker harness
- [json-glib](json-glib/README.md) — verified Docker harness
- [yajl](yajl/README.md) — verified Docker harness
- [cjson](cjson/README.md) — verified Docker harness
- [jq](jq/README.md) — verified Docker harness
- [libfastjson](libfastjson/README.md) — verified Docker harness
- [yyjson](yyjson/README.md) — verified Docker harness
- [json-parser](json-parser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
