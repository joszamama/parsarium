# JAVASCRIPT × TOML: selected parsers (pilot)

3 control-verified third-party paths selected. The ceiling is ten; ranks cover only verified paths from the bounded search. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

npm downloads over the last month (2026-10-18 to 2026-11-16), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [smol-toml](https://github.com/squirrelchat/smol-toml/blob/v1.9.1/README.md#usage) | 1.9.1 | 252,264,468 | One TOML 1.0.0 document from local bytes decoded as strict UTF-8 via `parse(text, { integersAsBigInt: true })`; integers are BigInt, floats Number, date-times TomlDate with kind flags | smol-toml (own hand-written parser) |
| 2 | [toml-eslint-parser](https://github.com/ota-meshi/toml-eslint-parser/blob/6008e35499342f1116262162d16dbcab0c84760c/README.md#usage-for-directly) | 1.0.3 | 7,684,028 | One TOML 1.0.0 document from local bytes decoded as strict UTF-8 via `parseTOML(text, { tomlVersion: '1.0.0' })`; typed tree from the syntax tree's resolved table keys and typed value nodes | toml-eslint-parser (own tokenizer and syntax-tree parser) |
| 3 | [@ltd/j-toml](https://github.com/LongTengDao/j-toml/blob/e946ce04db3d72ce59653c4e3daad86681f1de37/README.md) | 1.38.0 | 948,738 | One TOML 1.0.0 document from local bytes decoded as strict UTF-8 via `TOML.parse[1.0](text, { joiner: '\n', bigint: true })`; integers are BigInt, floats Number, date-times j-toml's OffsetDateTime/LocalDateTime/LocalDate/LocalTime classes | j-toml (LongTengDao; own line-iterator parser) |

Node.js has no TOML API ([standard.json](standard.json)).

Each path turns both valid controls into the exact typed tree of `catalog/toml/PROTOCOL.md` ([verification.json](verification.json)). smol-toml parses with its own code in `dist/parse.js`, `dist/struct.js`, `dist/extract.js` and `dist/primitive.js`; toml-eslint-parser runs its own tokenizer and parser in `lib/index.mjs`; @ltd/j-toml runs its own line-iterator parser and literal decoders in `index.mjs`, with `bigint: true` (integers as BigInt) and `joiner: '\n'` (multi-line string lines joined with LF). They share no code. AFL++ feedback is scoped to each package's V8 source ranges; three repeats per control are identical, and the controls differ by 118 tuples (smol-toml), 156 tuples (toml-eslint-parser) and 98 tuples (@ltd/j-toml) ([afl-feedback.json](afl-feedback.json)). @ltd/j-toml covers 1,512 package lines on service-config and 1,536 on typed-scalars; its offset date-times are read with millisecond precision through the documented `getUTC*` getters.

Unverified leads: `confbox` 0.3.2 (414,804,968 downloads) is a smol-toml wrapper: its `parseTOML` calls a minified bundled copy of smol-toml without options, so integers and floats are plain Numbers and the typed-scalars float `exponent = 1e3` comes back as the Number 1000, the same as integer 1000; service-config matches. `toml` 5.0.1 (164,115,023) fails typed-scalars on the same float and returns local date-times, dates and times as plain strings. `@iarna/toml` 2.2.5 (46,454,916) keeps date kinds but fails typed-scalars on the same float. `@decimalturn/toml-patch` (503,811), `@taplo/lib` (408,802, WebAssembly), `js-toml` (198,933), `toml-j0.4` (59,237) and `fast-toml` (23,058) were not run. Evidence is in [leads.json](leads.json).
