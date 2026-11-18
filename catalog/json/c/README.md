# JSON / C — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Nine C JSON third-party paths pass two valid controls with format-aware tree results, parser source coverage and stable AFL++ feedback. The original Conan recipe search missed Debian-packaged C parsers; a bounded Debian source-name search for 'json' (320 hits) plus exact lookups for jansson, jq, frozen, jsmn and parson in the same hashed popcon snapshot found the Debian-packaged C parser leads. A later exact-lookup pass found yajl (152,183), which the json-name search missed because its source name lacks 'json'; yajl is checked through its documented yajl_parse callback API, and its parser-only AFL++ probe uses CLASSIC instrumentation because the default PCGUARD build crashed on the valid controls on arm64. libfastjson is a json-c fork and shares the json-c tokener family; jq's count is the jq source package (mostly the command-line program), and its jv C API is documented on the project wiki without a stability commitment; jq numbers have one kind, so integer/float in its tree comes from the preserved decimal literal. frozen fails the nested-object control (\u00e9 decoded to one Latin-1 byte), jsmn is tokenizer-only, liblaxjson (1 installation) fails the nested-object control (it requires an explicit exponent sign) and reports every number as a double, and parson (no Debian source) has no primary value. Debian installations mostly reflect dependencies and miss vendored copies. The json-name search (320 hits) and twenty-five exact source-name lookups in the same snapshot leave no other positive-count C JSON value library, and no C JSON source qualifies for the format-specific dev-package fallback. These paths do not establish a definitive top ten or full RFC 8259 compliance. ISO C documents no JSON API. Round 4 (2026-11-18) tried discovery routes beyond the name search and exact lookups: Debian apt-cache search 'json' over binary package names and descriptions (every C JSON library is already selected or decided; sqlite3's SQL json functions fall under the multi-purpose rule), vcpkg, Homebrew and Conan package lists (nanojsonc and parson, not in Debian) and a GitHub 'json parser' search for C (unpackaged parsers without a Debian value). No Debian-ranked path was added (registry snapshot, round_4_discovery). Round 5 (2026-11-18) rechecked the tree-sitter grammars after tree-sitter-sql was accepted in C SQL: the only Debian JSON grammar, tree-sitter-json 0.24.8-3 (7 installations), keeps string escapes undecoded in its syntax tree, so under the tree-sitter rule in PROTOCOL.md it stays excluded with jsmn, (registry snapshot, round_5_tree_sitter). Round 6 (2026-11-18): PROTOCOL.md now lets C and C++ cells fill slots left after the primary and Debian paths with tagged upstream releases of format-specific parser repositories with at least 100 GitHub stars, ranked separately by stars. Bounded GitHub searches (three queries, first 100 results each) and the earlier leads gave the star order jsmn (4,215, tokenizer only), sj.h (1,556, no tag), parson (1,481, no tag or release, so its verified candidate commit cannot be pinned), lua-cjson (1,001, a Lua module) and json.h (846, tag pre-ai). json.h passes both controls and the parser-scoped AFL++ gate and takes the tenth slot as a supplemental path; its stars are repository interest, not downloads, and are not comparable to the nine Debian counts (registry snapshot, round_6_star_fallback). json.h keeps numbers as their source text, so its integer/float kinds come from the stored literal.

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
- [json.h](json-h/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
