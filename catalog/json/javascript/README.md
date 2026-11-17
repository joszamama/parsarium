# JSON / JavaScript — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 1 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: stream-json 3.9.0 (56,997,988 npm downloads) and bfj 9.1.4 (18,016,242) are separate parser families with documented local stream APIs, valid nested-object and nested-array controls, parser-source coverage, and input-dependent AFL++ feedback. jsonparse (105,362,611) has its own Buffer parser but no documented API and remains unresolved; json5, jsonc-parser, and json-bigint have higher downloads but string-only APIs and/or superset grammars under the current protocol. Six high-download packages delegate to JSON.parse. Downloads were fetched for 24 hand-picked candidates, not every search hit. The standard JSON.parse path is counted separately; it has a staged function-entry AFL++ proxy, but no parser source lines or V8 basic-block edges. Two valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/javascript/json/ranking.md) · [Standard API inventory](../../../data/javascript/json/standard.json)

## Third-party parsers

- [stream-json](stream-json/README.md) — verified Docker harness
- [bfj](bfj/README.md) — verified Docker harness

## Standard and runtime APIs

- [JSON.parse(text) after new TextDecoder('utf-8', {fatal: true}).decode(Buffer)](standard/json-parse-text-after-new-textdecoder-utf-8-fatal-true-decode-buffer/README.md) — staged Docker control
