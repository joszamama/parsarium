# JSON / PHP — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 1 verified standard APIs, 2 verified Docker harnesses.

Two PHP JSON third-party paths passed valid nested object controls and source-line coverage. JSON Machine also passed a valid nested array control and stable source-line AFL feedback, but it shares the PHP ext/json value decoder with the runtime path. Six own-parser or partial-own-parser leads remain unverified; four json_decode wrappers are excluded. The bounded search used five Packagist queries of at most 100 hits each. Package downloads measure overall package adoption, not JSON parsing frequency. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/php/json/ranking.md) · [Standard API inventory](../../../data/php/json/standard.json)

## Third-party parsers

- [seld/jsonlint](seld-jsonlint/README.md) — verified Docker harness
- [halaxa/json-machine](halaxa-json-machine/README.md) — verified Docker harness

## Standard and runtime APIs

- [json_decode(string $json, ?bool $associative = null, int $depth = 512, int $flags = 0)](standard/json-decode-string-json-bool-associative-null-int-depth-512-int-flags-0/README.md) — verified Docker harness
