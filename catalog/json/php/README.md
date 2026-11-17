# JSON / PHP — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 1 verified standard APIs, 3 verified Docker harnesses.

Three PHP JSON third-party paths passed valid nested object controls and source-line coverage. Laminas and JSON Machine also passed a valid nested array control and stable source-line AFL feedback. Laminas is abandoned, and its own decoder runs only when explicitly enabled; its default API route delegates to ext/json. JSON Machine shares ext/json for member decoding. Five own-parser or partial-own-parser leads remain unverified; four json_decode wrappers are excluded. The bounded search used five Packagist queries of at most 100 hits each. Package downloads measure overall/historical adoption, not JSON parsing frequency. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/php/json/ranking.md) · [Standard API inventory](../../../data/php/json/standard.json)

## Third-party parsers

- [seld/jsonlint](seld-jsonlint/README.md) — verified Docker harness
- [laminas/laminas-json](laminas-laminas-json/README.md) — verified Docker harness
- [halaxa/json-machine](halaxa-json-machine/README.md) — verified Docker harness

## Standard and runtime APIs

- [json_decode(string $json, ?bool $associative = null, int $depth = 512, int $flags = 0)](standard/json-decode-string-json-bool-associative-null-int-depth-512-int-flags-0/README.md) — verified Docker harness
