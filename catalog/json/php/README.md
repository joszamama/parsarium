# JSON / PHP — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 1 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: PHP JSON parsing is dominated by the bundled ext/json json_decode; most popular Packagist JSON packages wrap it. Only seld/jsonlint, the highest-download package with its own pure-PHP parser, was built and control-verified. Its downloads are inflated by Composer, which depends on it but calls json_decode first and uses JsonParser for error reports. Seven own-parser or partial-own-parser leads are logged in leads.json and are not verified or ranked; four json_decode wrappers are excluded. Non-parser hits such as JWT, JSON Schema, JSONPath, JMESPath, serializers and JSON-RPC were not treated as leads. One valid nested object control does not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/php/json/ranking.md) · [Standard API inventory](../../../data/php/json/standard.json)

## Third-party parsers

- [seld/jsonlint](seld-jsonlint/README.md) — verified Docker harness

## Standard and runtime APIs

- [json_decode(string $json, ?bool $associative = null, int $depth = 512, int $flags = 0)](standard/json-decode-string-json-bool-associative-null-int-depth-512-int-flags-0/README.md) — verified Docker harness
