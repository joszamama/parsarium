# JSON / JavaScript — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 1 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one third-party path (stream-json 3.9.0, 56,997,988 npm downloads 2026-10-17 to 2026-11-15) was built, control-verified, and given parser-derived V8 AFL++ feedback. It is the highest-download lead found with its own RFC 8259 tokenizer and a documented local Buffer/stream API. jsonparse (105,362,611) has its own Buffer parser but no documented API and was not selected; json5, jsonc-parser, and json-bigint have higher downloads but string-only APIs and/or superset grammars. Six high-download packages delegate to JSON.parse. Downloads were fetched for 24 hand-picked candidates, not every search hit. The standard JSON.parse path is counted separately; V8 parses it natively, so it has a control receipt and a staged function-entry AFL++ proxy, but no parser source lines or V8 basic-block edges. Two valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/javascript/json/ranking.md) · [Standard API inventory](../../../data/javascript/json/standard.json)

## Third-party parsers

- [stream-json](stream-json/README.md) — verified Docker harness

## Standard and runtime APIs

- [JSON.parse(text) after new TextDecoder('utf-8', {fatal: true}).decode(Buffer)](standard/json-parse-text-after-new-textdecoder-utf-8-fatal-true-decode-buffer/README.md) — staged Docker control
