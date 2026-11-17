# JSON / JavaScript — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 1 verified standard APIs, 10 verified Docker harnesses.

Pilot cell: ten high-download package/API paths have valid nested-object and nested-array controls, package parser coverage, and AFL++ feedback; nine parser families are represented. jsonparse (105,362,611 downloads) has no API in its README; Parser.write(Buffer) is evidenced by packaged examples and tests. The adapter requires one root and checks the parser stack and tokenizer state. JSONStream (56,299,470 downloads) is a separate stream API path over the same pinned jsonparse 1.3.1 tokenizer, not an independent engine. JSONStream.parse([]) emits one root according to packaged code and tests despite its README statement. Its private parser exposes no end-of-input completeness check: the adapter requires one emitted root, no error, and stream end, but trailing unfinished syntax after a complete root may go undetected. JSONStream own package source is covered; differential feedback on the valid controls arises only in underlying jsonparse source. @humanwhocodes/momoa (18,038,222 downloads) has a documented string API only: the adapter decodes local bytes as strict UTF-8 and calls parse(text, {mode: 'json'}), which rejects tokens after the first value; the summary is taken from its AST nodes. @streamparser/json receives the entire Buffer and checks trailing bytes after the first root for whitespace. json5 is a JSON5 superset parser with its own lexer and state machine. It parses both valid strict JSON controls exactly through a documented text API, but accepts JSON5-only syntax and its high download count mainly reflects configuration-file use. json-bigint also has a documented string API: the adapter decodes local bytes strictly, then tags the parser's returned tree. Its Crockford-derived parser source is distinct from the other selected families; BigNumber behavior for long numeric tokens is not established by these controls. jsonc-parser adds a strict-option parseTree text API over its own Microsoft scanner/tree parser; both valid controls match but do not test JSONC extension rejection. lossless-json independently parses strict local UTF-8 text into type-tagged values whose numeric lexemes remain exact LosslessNumber strings; the two valid controls show parser-source coverage and stable input-dependent AFL++ feedback. Other high-download leads remain unresolved. Downloads cover 24 hand-picked candidates, not every search hit. Standard JSON.parse is separate. Two valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/javascript/json/ranking.md) · [Standard API inventory](../../../data/javascript/json/standard.json)

## Third-party parsers

- [json5](json5/README.md) — verified Docker harness
- [jsonc-parser](jsonc-parser/README.md) — verified Docker harness
- [json-bigint](json-bigint/README.md) — verified Docker harness
- [jsonparse](jsonparse/README.md) — verified Docker harness
- [stream-json](stream-json/README.md) — verified Docker harness
- [JSONStream](jsonstream/README.md) — verified Docker harness
- [@humanwhocodes/momoa](humanwhocodes-momoa/README.md) — verified Docker harness
- [bfj](bfj/README.md) — verified Docker harness
- [@streamparser/json](streamparser-json/README.md) — verified Docker harness
- [lossless-json](lossless-json/README.md) — verified Docker harness

## Standard and runtime APIs

- [JSON.parse(text) after new TextDecoder('utf-8', {fatal: true}).decode(Buffer)](standard/json-parse-text-after-new-textdecoder-utf-8-fatal-true-decode-buffer/README.md) — verified Docker harness
