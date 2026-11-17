# JSON / PHP — pilot

**Status:** pilot_nine_selected_search_bounded; incomplete. 9 verified third-party paths, 1 verified standard APIs, 9 verified Docker harnesses.

Nine PHP JSON third-party paths passed valid nested object controls and source-line coverage. Laminas, JSON Machine, salsify, pcrov and the four paths added from the extended search (boundwize/jsonrecast, laktak/hjson, klkvsk/json-decode-stream, eftec/services_json) also passed a valid nested array control and stable source-line AFL feedback. Laminas is abandoned, and its own decoder runs only when explicitly enabled; its default API route delegates to ext/json. JSON Machine shares ext/json for member decoding. salsify accepts only object/array roots and silently accepts concatenated documents, so its harness rejects anything other than one complete document; the tree-building listener is harness code. The own-parser lead joelwurtz/json-stream-polyfill and three low-download supplemental hits remain uninspected. bcncommerce/json-stream (lossy Reader, identical package lines on both controls) and symfony/json-streamer (a schema-free read is one json_decode call) are excluded after pinned probes; salsify forks and listener wrappers and json_decode wrappers, including colinodell/json5 on both valid controls, are excluded. pcrov/jsonreader has a separate lexer and state machine, with three parser-source features and AFL tuples differing between the valid controls. boundwize/jsonrecast builds a formatting-preserving AST with its own lexer and recursive-descent parser; string escapes are ext/json on single tokens, and most of its 35-line control differential is in the indentation-detection pass that parse() runs. laktak/hjson parses a JSON superset and is counted only for valid JSON; it drops an empty member name and lets duplicates overwrite by source reading. klkvsk/json-decode-stream unescapes string tokens with ext/json and accepts concatenated documents, which its adapter rejects. eftec/services_json returns null rather than an error for text it cannot reduce, and its 4-line control differential is the smallest among the selected PHP JSON paths. The bounded search used thirteen Packagist queries of at most 100 hits each: five captured at 03:23 UTC and eight supplemental queries (json stream, json5, jsonc, json lexer, json tokenizer, json reader, hjson, json pull parser) captured at 15:19 UTC. Packagist matches json5, jsonc and hjson loosely, so their first 100 hits are mostly generic JSON packages. Rankings use the 03:23 download values, which cover every selected path. Package downloads measure overall/historical adoption, not JSON parsing frequency. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/php/json/ranking.md) · [Standard API inventory](../../../data/php/json/standard.json)

## Third-party parsers

- [seld/jsonlint](seld-jsonlint/README.md) — verified Docker harness
- [laminas/laminas-json](laminas-laminas-json/README.md) — verified Docker harness
- [halaxa/json-machine](halaxa-json-machine/README.md) — verified Docker harness
- [salsify/json-streaming-parser](salsify-json-streaming-parser/README.md) — verified Docker harness
- [pcrov/jsonreader](pcrov-jsonreader/README.md) — verified Docker harness
- [boundwize/jsonrecast](boundwize-jsonrecast/README.md) — verified Docker harness
- [laktak/hjson](laktak-hjson/README.md) — verified Docker harness
- [klkvsk/json-decode-stream](klkvsk-json-decode-stream/README.md) — verified Docker harness
- [eftec/services_json](eftec-services-json/README.md) — verified Docker harness

## Standard and runtime APIs

- [json_decode(string $json, ?bool $associative = null, int $depth = 512, int $flags = 0)](standard/json-decode-string-json-bool-associative-null-int-depth-512-int-flags-0/README.md) — verified Docker harness
