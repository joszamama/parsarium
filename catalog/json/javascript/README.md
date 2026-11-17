# JSON / JavaScript — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 1 verified standard APIs, 4 verified Docker harnesses.

Pilot cell: four separate high-download parser families have local byte/stream APIs, valid nested-object and nested-array controls, parser-source coverage, and input-dependent AFL++ feedback. jsonparse (105,362,611 downloads) has no API in its README; its Parser.write(Buffer) path is taken from the packaged example and tests. It has no end() and accepts concatenated values, so the adapter rejects a second root, an open container or an unfinished token. JSONStream wraps jsonparse and is not counted separately. @streamparser/json receives the entire Buffer and its tokenizer checks trailing bytes after the first root for JSON whitespace. Other higher-download leads either use a string-only API, a superset grammar, or delegate to JSON.parse. Downloads were fetched for 24 hand-picked candidates, not every search hit. Standard JSON.parse is counted separately. Two valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/javascript/json/ranking.md) · [Standard API inventory](../../../data/javascript/json/standard.json)

## Third-party parsers

- [jsonparse](jsonparse/README.md) — verified Docker harness
- [stream-json](stream-json/README.md) — verified Docker harness
- [bfj](bfj/README.md) — verified Docker harness
- [@streamparser/json](streamparser-json/README.md) — verified Docker harness

## Standard and runtime APIs

- [JSON.parse(text) after new TextDecoder('utf-8', {fatal: true}).decode(Buffer)](standard/json-parse-text-after-new-textdecoder-utf-8-fatal-true-decode-buffer/README.md) — staged Docker control
