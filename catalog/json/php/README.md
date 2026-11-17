# JSON / PHP — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 1 verified standard APIs, 5 verified Docker harnesses.

Five PHP JSON third-party paths passed valid nested object controls and source-line coverage. Laminas, JSON Machine, salsify and pcrov also passed a valid nested array control and stable source-line AFL feedback. Laminas is abandoned, and its own decoder runs only when explicitly enabled; its default API route delegates to ext/json. JSON Machine shares ext/json for member decoding. salsify accepts only object/array roots and silently accepts concatenated documents, so its harness rejects anything other than one complete document; the tree-building listener is harness code. Two own-parser or partial-own-parser leads remain unverified; five json_decode wrappers are excluded, including colinodell/json5 on both valid controls. pcrov/jsonreader has a separate lexer and state machine, with three parser-source features and AFL tuples differing between the valid controls. The bounded search used five Packagist queries of at most 100 hits each. Package downloads measure overall/historical adoption, not JSON parsing frequency. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/php/json/ranking.md) · [Standard API inventory](../../../data/php/json/standard.json)

## Third-party parsers

- [seld/jsonlint](seld-jsonlint/README.md) — verified Docker harness
- [laminas/laminas-json](laminas-laminas-json/README.md) — verified Docker harness
- [halaxa/json-machine](halaxa-json-machine/README.md) — verified Docker harness
- [salsify/json-streaming-parser](salsify-json-streaming-parser/README.md) — verified Docker harness
- [pcrov/jsonreader](pcrov-jsonreader/README.md) — verified Docker harness

## Standard and runtime APIs

- [json_decode(string $json, ?bool $associative = null, int $depth = 512, int $flags = 0)](standard/json-decode-string-json-bool-associative-null-int-depth-512-int-flags-0/README.md) — verified Docker harness
