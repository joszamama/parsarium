# JAVASCRIPT × JSON: selected parsers (pilot)

6 control-verified third-party paths selected. The ceiling is ten; this pilot verifies six high-download local byte, stream or text API paths across five parser families, and does not pad the selection. JSONStream shares the jsonparse tokenizer. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

npm downloads over 2026-10-17 to 2026-11-15 (30 days), observed 2026-11-17T03:16:41Z ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jsonparse](https://github.com/creationix/jsonparse/blob/1480064a3040cec3f27aa929dd1d1469150b8737/examples/twitterfeed.js) | 1.3.1 | 105,362,611 | One JSON value from local bytes via `Parser.write(Buffer)`; adapter requires exactly one complete root | jsonparse byte-level tokenizer and stack value builder |
| 2 | [stream-json](https://github.com/uhop/stream-json/wiki/Parser) | 3.9.0 | 56,997,988 | One RFC 8259 JSON text from local bytes via parser() and Assembler | stream-json charCodeAt/regex streaming tokenizer |
| 3 | [JSONStream](https://github.com/dominictarr/JSONStream/blob/0593d4b4e6c63c6c0e2e68463538fd83bd1eb964/test/test2.js) | 1.3.5 | 56,299,470 | One emitted JSON root from local bytes via `JSONStream.parse([])` and `stream.end(Buffer)`; trailing unfinished syntax after that root can go undetected | jsonparse byte-level tokenizer (shared with rank 1) under JSONStream path filter |
| 4 | [@humanwhocodes/momoa](https://github.com/humanwhocodes/momoa/blob/625bcbec28623ccebb1da837c71389cf38014800/js/README.md#parsing) | 3.3.13 | 18,038,222 | One complete JSON text from local bytes decoded as strict UTF-8 and passed to `parse(text, {mode: 'json'})`; trailing tokens rejected | momoa tokenizer and recursive-descent AST parser |
| 5 | [bfj](https://www.npmjs.com/package/bfj?activeTab=readme) | 9.1.4 | 18,016,242 | One complete JSON text from a local `Readable` via `parse(stream, {ndjson:false})` | bfj asynchronous JSON walker |
| 6 | [@streamparser/json](https://www.npmjs.com/package/@streamparser/json?activeTab=readme) | 0.0.26 | 13,886,478 | One complete JSON document from local UTF-8 bytes via `JSONParser.write`; tokenizer checks trailing bytes for whitespace | @streamparser/json TypeScript tokenizer and token parser |

jsonparse's README documents no API. Its `new Parser()`, `onValue` and `write(chunk)` call pattern comes from the packaged example and tests at the tarball's gitHead. The parser has no `end()` call and accepts a stream of concatenated values, so the adapter writes the whole local Buffer once and then requires exactly one `onValue` with an empty stack, no open container, and the tokenizer back in its START state. From source reading (not run on such inputs), numbers are any run of digits, `.`, `e`, `E`, `+` and `-` checked only by `Number()`, so leading zeros are not rejected, and integer digit strings that do not round-trip through `Number` are emitted as strings. JSONStream 1.3.5 is a separate package API path over jsonparse 1.3.1 and through 2.3.8, all pinned by npm integrity and tarball SHA-256. Its own `index.js` filters and emits roots; jsonparse tokenizes and builds values. The README says an empty path emits no data, while the pinned code and packaged test emit one completed root; the adapter follows that test. The private parser has no end-of-input completeness check, so a trailing unfinished token or open container after one completed root can go undetected. V8 covers 48 JSONStream source lines, 293 jsonparse lines, and 76 through lines on the first valid control. The 17 changed AFL source ranges and tuples between controls are all in jsonparse; JSONStream own source features are identical. It is counted as a package path, not another parser engine ([feedback report](jsonstream-afl-feedback.json)).

@humanwhocodes/momoa 3.3.13 (Apache-2.0, npm integrity and tarball SHA-256 pinned) documents `parse(text)` on a string, with `"json"` as the default mode. The adapter reads the local bytes, decodes them with a strict UTF-8 `TextDecoder` that keeps a BOM, and calls `parse(text, {mode: 'json'})` once; momoa throws on any token after the first value. The bundled `dist/momoa.js` holds its own character-level tokenizer and recursive-descent parser and does not call `JSON.parse`. The summary is built from momoa's AST nodes rather than `evaluate()`, and an independent Python `json` summary of the same control bytes gives the same result. V8 marks 1,590 `dist/momoa.js` lines on the first valid control by the shared line method, which counts every non-blank line inside an executed range, so comments in the module body count. The AFL++ bridge repeats stably (126/146 and 111/131 features/tuples); the second control changes 17 ranges, all in `dist/momoa.js` (string escape and `\u` handling, negative and fractional numbers, line tracking), and 17 tuples. On 2026-11-17 the 30-day value was unchanged, and the npm last-week value (2026-11-09 to 2026-11-15) was 4,871,887, above bfj's 4,518,652, so the rank order holds on both windows.

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [JSON.parse(text)](https://tc39.es/ecma262/#sec-json.parse) after strict UTF-8 [TextDecoder](https://nodejs.org/download/release/v26.10.0/docs/api/util.html#class-utiltextdecoder) | Node.js 26.10.0 | V8 native JSON.parse |

`JSON.parse` takes a string, so the adapter decodes bytes first. V8 implements it natively. A staged AFL++ bridge maps observed `JsonParser` function entries into tuples; it does not provide parser source lines or V8 basic-block edges ([bridge receipt](../../../fuzzing/afl-native/json/javascript/stdlib_json_parse/verification.json)).

## Lead log

Numeric leads from the same snapshot. jsonparse, JSONStream and @humanwhocodes/momoa were promoted to the verified ranking above; the remaining entries are not verified and not selected. Schema, pointer, stringify, comment-stripping, and loader hits were not treated as parser leads.

| Lead | Version seen | Downloads (30 days) | Kind | Status |
| --- | --- | ---: | --- | --- |
| [json5](https://www.npmjs.com/package/json5) | 2.2.3 | 1,214,931,394 | own parser not selected | Own JSON5 parser (no JSON.parse call in 2.2.3 tarball). JSON5 is a superset grammar and the documented JSON5.parse(text) takes a string; not an RFC 8259 byte/stream path. |
| [parse-json](https://www.npmjs.com/package/parse-json) | 8.3.0 | 707,041,225 | delegates to json parse | index.js calls JSON.parse and adds error context; shares the V8 JSON.parse family counted under standard. |
| [json-parse-even-better-errors](https://www.npmjs.com/package/json-parse-even-better-errors) | 6.0.0 | 575,810,233 | delegates to json parse | lib/index.js calls JSON.parse and adds error context; shares the V8 JSON.parse family. |
| [jsonc-parser](https://www.npmjs.com/package/jsonc-parser) | 3.3.1 | 401,936,432 | own parser not selected | Own scanner/parser (no JSON.parse call in 3.3.1). JSONC grammar (comments, optional trailing commas) and documented parse(text: string); no local Buffer/stream API. Not run. |
| [json-bigint](https://www.npmjs.com/package/json-bigint) | 1.0.0 | 297,771,552 | own parser not selected | Own recursive-descent parse (JSON.parse appears only in stringify.js). Documented parse(text) takes a string; no Buffer/stream API. Not run. |
| [secure-json-parse](https://www.npmjs.com/package/secure-json-parse) | 4.1.1 | 222,970,191 | delegates to json parse | index.js calls JSON.parse and then scans for prototype keys; shares the V8 JSON.parse family. |
| [@discoveryjs/json-ext](https://www.npmjs.com/package/@discoveryjs/json-ext) | 1.1.0 | 111,091,175 | delegates to json parse | parseChunked accepts streams/iterables but src/parse-chunked.js decodes each value fragment with JSON.parse; shares the V8 JSON.parse family. |
| [jsonparse](https://www.npmjs.com/package/jsonparse) | 1.3.1 | 105,362,611 | own parser | Promoted to verified: own byte-level tokenizer behind Parser.write(Buffer); README documents no API, so the call pattern comes from the packaged example and tests. Both valid controls match exactly. |
| [comment-json](https://www.npmjs.com/package/comment-json) | 5.0.0 | 92,360,031 | own parser not selected | Uses an esprima tokenizer and calls JSON.parse on individual token values (src/parse.js); JSON-with-comments grammar and string API. Not run. |
| [jju](https://www.npmjs.com/package/jju) | 1.4.0 | 67,730,650 | own parser not selected | Own recursive JSON5 parser (JSON.parse appears only in a comment); string API, JSON5 grammar. Not run. |
| [JSONStream](https://www.npmjs.com/package/JSONStream) | 1.3.5 | 56,299,470 | wrapper over shared parser | Promoted to verified as a separate package API path over jsonparse; the two valid controls emit exact roots, while the parser family is shared. |
| [partial-json](https://www.npmjs.com/package/partial-json) | 0.1.7 | 55,052,021 | not a value parser path | Parser for incomplete JSON (e.g. truncated LLM output); dist calls JSON.parse; string API. Not run. |
| [@hapi/bourne](https://www.npmjs.com/package/@hapi/bourne) | 4.0.1 | 25,603,025 | delegates to json parse | src/index.js calls JSON.parse and then scans for prototype keys; shares the V8 JSON.parse family. |
| [fast-json-parse](https://www.npmjs.com/package/fast-json-parse) | 1.0.3 | 24,460,907 | delegates to json parse | parse.js wraps JSON.parse in try/catch; shares the V8 JSON.parse family. |
| [jsonrepair](https://www.npmjs.com/package/jsonrepair) | 3.15.0 | 21,639,676 | not a value parser path | Repairs malformed JSON text into JSON text; not a value parser path. Not run. |
| [@humanwhocodes/momoa](https://www.npmjs.com/package/@humanwhocodes/momoa) | 3.3.13 | 18,038,222 | own parser | Promoted to verified: own tokenizer and AST parser behind the documented `parse(text)`; the adapter decodes local bytes as strict UTF-8 first. Both valid controls match exactly. |
| [lossless-json](https://www.npmjs.com/package/lossless-json) | 4.3.3 | 9,738,476 | own parser not selected | Own parser (JSON.parse appears only in a doc comment); documented parse(text) takes a string. Not run. |
| [json-source-map](https://www.npmjs.com/package/json-source-map) | 0.6.1 | 5,940,263 | own parser not selected | Own parser producing pointer maps; string API. Not run. |
| [clarinet](https://www.npmjs.com/package/clarinet) | 0.12.6 | 2,486,814 | own parser not selected | Own SAX-style parser; write(string) chunks. Not run. |
| [oboe](https://www.npmjs.com/package/oboe) | 2.1.7 | 2,129,406 | not a value parser path | Streaming JSON loader built on clarinet; would share that family. Not run. |
| [json-to-ast](https://www.npmjs.com/package/json-to-ast) | 2.1.0 | 2,079,219 | own parser not selected | Own AST parser; string API. Not run. |

Queries: `json parser`, `json parse`, `streaming json parser`, `json tokenizer`, `json`; limit 100 each; 500 hits, 454 unique. `jsonparse`'s missing README API is the main selection judgement: it is counted on the strength of its packaged example and tests; see [leads.json](leads.json).
