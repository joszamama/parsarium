# JAVASCRIPT × JSON: selected parsers (pilot)

1 control-verified third-party path selected. The ceiling is ten; this pilot builds only the highest-download lead that has its own RFC 8259 parser and a documented local Buffer/stream API, and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

npm downloads over 2026-10-17 to 2026-11-15 (30 days), observed 2026-11-17T03:16:41Z ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [stream-json](https://github.com/uhop/stream-json/wiki/Parser) | 3.9.0 | 56,997,988 | One RFC 8259 JSON text from local bytes via parser() and Assembler | stream-json charCodeAt/regex streaming tokenizer |

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [JSON.parse(text)](https://tc39.es/ecma262/#sec-json.parse) after strict UTF-8 [TextDecoder](https://nodejs.org/download/release/v26.10.0/docs/api/util.html#class-utiltextdecoder) | Node.js 26.10.0 | V8 native JSON.parse |

`JSON.parse` takes a string, so the adapter decodes bytes first. V8 implements it natively; no parser source lines or AFL++ feedback are attributed to it.

## Lead log

Numeric leads from the same snapshot, not verified and not selected. Schema, pointer, stringify, comment-stripping, and loader hits were not treated as parser leads.

| Lead | Version seen | Downloads (30 days) | Kind | Status |
| --- | --- | ---: | --- | --- |
| [json5](https://www.npmjs.com/package/json5) | 2.2.3 | 1,214,931,394 | own parser not selected | Own JSON5 parser (no JSON.parse call in 2.2.3 tarball). JSON5 is a superset grammar and the documented JSON5.parse(text) takes a string; not an RFC 8259 byte/stream path. |
| [parse-json](https://www.npmjs.com/package/parse-json) | 8.3.0 | 707,041,225 | delegates to json parse | index.js calls JSON.parse and adds error context; shares the V8 JSON.parse family counted under standard. |
| [json-parse-even-better-errors](https://www.npmjs.com/package/json-parse-even-better-errors) | 6.0.0 | 575,810,233 | delegates to json parse | lib/index.js calls JSON.parse and adds error context; shares the V8 JSON.parse family. |
| [jsonc-parser](https://www.npmjs.com/package/jsonc-parser) | 3.3.1 | 401,936,432 | own parser not selected | Own scanner/parser (no JSON.parse call in 3.3.1). JSONC grammar (comments, optional trailing commas) and documented parse(text: string); no local Buffer/stream API. Not run. |
| [json-bigint](https://www.npmjs.com/package/json-bigint) | 1.0.0 | 297,771,552 | own parser not selected | Own recursive-descent parse (JSON.parse appears only in stringify.js). Documented parse(text) takes a string; no Buffer/stream API. Not run. |
| [secure-json-parse](https://www.npmjs.com/package/secure-json-parse) | 4.1.1 | 222,970,191 | delegates to json parse | index.js calls JSON.parse and then scans for prototype keys; shares the V8 JSON.parse family. |
| [@discoveryjs/json-ext](https://www.npmjs.com/package/@discoveryjs/json-ext) | 1.1.0 | 111,091,175 | delegates to json parse | parseChunked accepts streams/iterables but src/parse-chunked.js decodes each value fragment with JSON.parse; shares the V8 JSON.parse family. |
| [jsonparse](https://www.npmjs.com/package/jsonparse) | 1.3.1 | 105,362,611 | own parser not selected | Own byte-level streaming parser with Parser.write(Buffer) in 1.3.1 source, and higher downloads than stream-json. Not selected because its README documents no API (it only says it is a streaming JSON parser); usage appears only in bundled examples. Strongest unresolved lead. |
| [comment-json](https://www.npmjs.com/package/comment-json) | 5.0.0 | 92,360,031 | own parser not selected | Uses an esprima tokenizer and calls JSON.parse on individual token values (src/parse.js); JSON-with-comments grammar and string API. Not run. |
| [jju](https://www.npmjs.com/package/jju) | 1.4.0 | 67,730,650 | own parser not selected | Own recursive JSON5 parser (JSON.parse appears only in a comment); string API, JSON5 grammar. Not run. |
| [JSONStream](https://www.npmjs.com/package/JSONStream) | 1.3.5 | 56,299,470 | not a value parser path | Stream filter wrapper over jsonparse; would share the jsonparse parser family. |
| [partial-json](https://www.npmjs.com/package/partial-json) | 0.1.7 | 55,052,021 | not a value parser path | Parser for incomplete JSON (e.g. truncated LLM output); dist calls JSON.parse; string API. Not run. |
| [@hapi/bourne](https://www.npmjs.com/package/@hapi/bourne) | 4.0.1 | 25,603,025 | delegates to json parse | src/index.js calls JSON.parse and then scans for prototype keys; shares the V8 JSON.parse family. |
| [fast-json-parse](https://www.npmjs.com/package/fast-json-parse) | 1.0.3 | 24,460,907 | delegates to json parse | parse.js wraps JSON.parse in try/catch; shares the V8 JSON.parse family. |
| [jsonrepair](https://www.npmjs.com/package/jsonrepair) | 3.15.0 | 21,639,676 | not a value parser path | Repairs malformed JSON text into JSON text; not a value parser path. Not run. |
| [@humanwhocodes/momoa](https://www.npmjs.com/package/@humanwhocodes/momoa) | 3.3.13 | 18,038,222 | own parser not selected | Own JSON tokenizer and AST parser (no JSON.parse call in 3.3.13); documented parse(text) takes a string. Not run. |
| [bfj](https://www.npmjs.com/package/bfj) | 9.1.4 | 18,016,242 | own parser not selected | Own asynchronous streaming walker (no JSON.parse call in 9.1.4) with documented stream input; control not run in this one-package pilot. |
| [@streamparser/json](https://www.npmjs.com/package/@streamparser/json) | 0.0.26 | 13,886,478 | own parser not selected | Own streaming tokenizer/parser (no JSON.parse call in 0.0.26); documented write(Uint8Array|string). Control not run in this one-package pilot. |
| [lossless-json](https://www.npmjs.com/package/lossless-json) | 4.3.3 | 9,738,476 | own parser not selected | Own parser (JSON.parse appears only in a doc comment); documented parse(text) takes a string. Not run. |
| [json-source-map](https://www.npmjs.com/package/json-source-map) | 0.6.1 | 5,940,263 | own parser not selected | Own parser producing pointer maps; string API. Not run. |
| [clarinet](https://www.npmjs.com/package/clarinet) | 0.12.6 | 2,486,814 | own parser not selected | Own SAX-style parser; write(string) chunks. Not run. |
| [oboe](https://www.npmjs.com/package/oboe) | 2.1.7 | 2,129,406 | not a value parser path | Streaming JSON loader built on clarinet; would share that family. Not run. |
| [json-to-ast](https://www.npmjs.com/package/json-to-ast) | 2.1.0 | 2,079,219 | own parser not selected | Own AST parser; string API. Not run. |

Queries: `json parser`, `json parse`, `streaming json parser`, `json tokenizer`, `json`; limit 100 each; 500 hits, 454 unique. `jsonparse`'s documented-API gap is the main selection judgement; see [leads.json](leads.json).
