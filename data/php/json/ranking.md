# PHP × JSON: selected parsers (pilot)

8 control-verified third-party paths selected. The ceiling is ten; this pilot does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

PHP code mostly parses JSON with the bundled `json_decode` (ext/json). The most downloaded Packagist JSON helpers wrap it, so they are excluded from the third-party ranking rather than counted as separate parsers.

## Primary within-cell adoption metric

Packagist total downloads, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [seld/jsonlint](https://packagist.org/packages/seld/jsonlint) | 1.12.2 | 252,371,311 | JSON text into stdClass/array/scalars | seld/jsonlint Lexer and LR table parser |
| 2 | [laminas/laminas-json](https://packagist.org/packages/laminas/laminas-json) | 3.8.0 | 35,102,503 | JSON text decoded with explicitly enabled own PHP Decoder | Laminas JSON Decoder (Zend lineage) |
| 3 | [halaxa/json-machine](https://packagist.org/packages/halaxa/json-machine) | 1.2.6 | 30,443,415 | Top-level object/array members; values decoded by ext/json | JSON Machine Lexer/Parser plus PHP ext/json |
| 4 | [salsify/json-streaming-parser](https://packagist.org/packages/salsify/json-streaming-parser) | v8.3.1 | 7,715,575 | One object/array root read from a stream; listener events built into values | salsify JsonStreamingParser state machine |
| 5 | [pcrov/jsonreader](https://packagist.org/packages/pcrov/jsonreader) | 1.0.4 | 1,520,757 | Local JSON bytes through its pull reader; exact object and array trees | pcrov JSON lexer and reader state machine |
| 6 | [boundwize/jsonrecast](https://packagist.org/packages/boundwize/jsonrecast) | 1.0.37 | 702,666 | One JSON text via `JsonRecast::parse(string)`; AST walked into an exact ordered type-tagged tree | boundwize/jsonrecast Lexer and recursive-descent JsonParser (formatting-preserving AST) |
| 7 | [laktak/hjson](https://packagist.org/packages/laktak/hjson) | v2.3.1 | 262,430 | One JSON text via `HJSONParser::parse(string)`, default options; exact ordered type-tagged tree | hjson-php HJSONParser (port of hjson-js) recursive character parser |
| 8 | [klkvsk/json-decode-stream](https://packagist.org/packages/klkvsk/json-decode-stream) | v1.0.3 | 68,854 | One JSON document via `Parser::fromString(string)->items()`; exact ordered type-tagged tree; file and stream sources cross-checked | klkvsk json-decode-stream Tokenizer, event Parser and Collector |

Composer depends on seld/jsonlint, which inflates the download count. Composer calls `json_decode` first and uses `JsonParser` to report errors. Laminas is abandoned; its default API route calls ext/json, so this adapter explicitly enables its own PHP Decoder. JSON Machine has an independent streaming parser for member boundaries, but the selected decoder delegates each member value to PHP ext/json. salsify decodes strings, escapes and numbers in its own code; the adapter supplies a listener that builds objects and lists, and rejects input that does not end exactly one document. pcrov/jsonreader has its own pull lexer and state machine; both valid controls match an independent type-tagged JSON tree, and its parser-only AFL bridge changes three source features and three tuples between them.

boundwize/jsonrecast 1.0.37 documents `JsonRecast::parse(string)`, which returns an editable, formatting-preserving AST. Its own lexer, number scanner and recursive-descent parser build the tree; each string token, quotes included, is unescaped by `json_decode`, while structure, member order, literals and numbers stay in package code (`NumberNode::toIntOrFloat()` casts the raw lexeme). Both valid controls match the independent Python `json` oracle with member order and integer/float kinds. Xdebug covers 421 package lines on the object control; the parser-line AFL++ bridge is stable on repeat and differs by 35 lines and 35 tuples between the controls. 26 of those lines are in `IndentDetector`, the formatting metadata pass that `parse()` runs, and 9 in the lexer, parser and number scanner ([receipt](boundwize-jsonrecast-feedback-differential.json)). The package was first released in 2026; its download count may be driven by a few dependents.

laktak/hjson v2.3.1 (hjson-php, a port of hjson-js) documents `HJSONParser::parse($text)` for JSON or Hjson text. Its own recursive parser walks UTF-8 characters, decodes escapes and `\u` sequences itself and reads numbers with `HJSONUtils::tryParseNumber`; with default options it never calls `json_decode`. Both valid controls match the independent Python `json` oracle with member order and integer/float kinds. Hjson is a superset of JSON (quoteless strings, comments, optional commas and root braces), so this path parses valid JSON but does not reject invalid RFC 8259 input, and the download count mainly reflects configuration-file use. Xdebug covers 201 package lines on the object control; the parser-line AFL++ bridge is stable on repeat and differs by 13 lines and 13 tuples, all in `HJSONParser.php` and `HJSONUtils.php` ([receipt](laktak-hjson-feedback-differential.json)).

klkvsk/json-decode-stream v1.0.3 documents `Parser::fromString()`, `fromFile()` and `fromStream()` with `items($selector)`; with no selector it yields each complete top-level document. Its own tokenizer, event parser and collector handle structure, literals and numbers (a strict regex, then `intval` or `doubleval`); each completed string token is unescaped by `json_decode('"' . $raw . '"')`. The adapter requires exactly one document. Both valid controls match the independent Python `json` oracle with member order and integer/float kinds, and the local file and stream sources give the same trees. Xdebug covers 358 package lines on the object control; the parser-line AFL++ bridge is stable on repeat and differs by 22 lines and 22 tuples, all in `Parser.php` ([receipt](klkvsk-json-decode-stream-feedback-differential.json)).

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [json_decode](https://www.php.net/manual/en/function.json-decode.php) | PHP 8.5.12 | PHP ext/json re2c scanner and Bison parser |

## Lead log

Numeric leads from the same snapshot, not verified and not selected. JWT, JSON Schema, JSONPath, JMESPath, serializer, and JSON-RPC hits were not treated as parser leads.

| Lead | Version seen | Packagist downloads | Status | Note |
| --- | --- | ---: | --- | --- |
| [colinodell/json5](https://packagist.org/packages/colinodell/json5) | v3.0.0 | 32,796,867 | excluded | [Both valid JSON controls](colinodell-json5-lead-check.json) return through ext/json; no own JSON5 parser lines run. This is not an independent parser path for the selected format. |
| [zendframework/zend-json](https://packagist.org/packages/zendframework/zend-json) | 3.1.2 | 24,719,945 | excluded | Pinned probe: default decode is ext/json `json_decode`; the optional builtin Decoder is the predecessor of the selected laminas-json Decoder. Shared family ([evidence](zendframework-zend-json-lead-check.json)). |
| [cerbero/json-parser](https://packagist.org/packages/cerbero/json-parser) | 1.1.1 | 823,332 | excluded | Own lexer; both valid controls match a Python json oracle, but Xdebug lines and AFL++ tuples are identical on both controls (0 difference). Fails the parser-feedback gate ([evidence](cerbero-json-parser-lead-check.json)). |
| [nette/utils](https://packagist.org/packages/nette/utils) | v4.1.6 | 514,679,287 | excluded | Nette\Utils\Json::decode is a json_decode wrapper; shares the verified ext/json family. |
| [symfony/serializer](https://packagist.org/packages/symfony/serializer) | v8.2.0-BETA2 | 384,296,452 | excluded | JsonDecode encoder calls json_decode; shares the verified ext/json family. |
| [beste/json](https://packagist.org/packages/beste/json) | 1.8.0 | 36,059,399 | excluded | Json::decode helper over json_decode; shares the verified ext/json family. |
| [ergebnis/json](https://packagist.org/packages/ergebnis/json) | 1.7.0 | 33,479,596 | excluded | Json value object validated through json_decode; shares the verified ext/json family. |
| [ghostwriter/json](https://packagist.org/packages/ghostwriter/json) | 3.0.3 | 5,844,205 | excluded | Json::decode wraps json_decode; ext/json family. |
| [herrera-io/json](https://packagist.org/packages/herrera-io/json) | 3.0.1 | 4,565,858 | excluded | Same release as kherge/json: json_decode, with seld/jsonlint only for error messages. |
| [bcncommerce/json-stream](https://packagist.org/packages/bcncommerce/json-stream) | 0.4.2 | 2,529,296 | excluded | Pinned probe: Reader::read() returns `{}` and `[]` alike and every number as a float, so neither control matches; Xdebug runs the same 143 lines on both controls. Its event Parser is salsify lineage ([evidence](bcncommerce-json-stream-lead-check.json)). |
| [maxakawizard/json-collection-parser](https://packagist.org/packages/maxakawizard/json-collection-parser) | 1.10.1 | 966,052 | excluded | Listener over salsify/json-streaming-parser; shared selected family. |
| [symfony/json-streamer](https://packagist.org/packages/symfony/json-streamer) | v8.1.10 | 946,545 † | excluded | Pinned probe: with the schema-free `Type::mixed()` the generated reader is one json_decode call with associative arrays; both controls lose `{}`/`[]` and run the same 129 package lines ([evidence](symfony-json-streamer-lead-check.json)). |
| [webmozart/json](https://packagist.org/packages/webmozart/json) | 1.2.2 | 884,156 | excluded | json_decode, with seld/jsonlint only for error messages. |
| [karriere/json-decoder](https://packagist.org/packages/karriere/json-decoder) | v5.1.0 | 474,219 | excluded | Maps one json_decode result onto classes. |
| [kherge/json](https://packagist.org/packages/kherge/json) | 3.0.1 | 259,958 | excluded | json_decode, with seld/jsonlint only for error messages. |
| [clue/json-stream](https://packagist.org/packages/clue/json-stream) | v0.1.1 | 249,068 | excluded | Buffers to a closing bracket and calls json_decode. |
| [rodenastyle/stream-parser](https://packagist.org/packages/rodenastyle/stream-parser) | v2.0.3 | 213,447 | excluded | JSON through maxakawizard/json-collection-parser, so salsify. |
| [janeklb/json-char-input-reader](https://packagist.org/packages/janeklb/json-char-input-reader) | v0.3.2 | 53,219 | excluded | Finds chunk boundaries only; the caller decodes the text. |
| [im0rtality/jsonstreamingparser](https://packagist.org/packages/im0rtality/jsonstreamingparser) | v4.0.0 | 37,399 | excluded | 2014 fork of the salsify parser. |
| [eftec/services_json](https://packagist.org/packages/eftec/services_json) | 2.5 | 35,783 | unresolved | Pure-PHP PEAR Services_JSON port; screening probe matched both controls exactly. |
| [cerbero/json-objects](https://packagist.org/packages/cerbero/json-objects) | v1.2.0 | 32,702 | excluded | Listeners over salsify/json-streaming-parser. |
| [viktorf/json-file-parser](https://packagist.org/packages/viktorf/json-file-parser) | 1.0.6 | 21,358 | excluded | Cuts raw object text by brace counting; curly-brace string offsets do not compile on PHP 8. |
| [joelwurtz/json-stream-polyfill](https://packagist.org/packages/joelwurtz/json-stream-polyfill) | 0.1.0 | 20,698 | unresolved | Own structural scanner; scalars and materialization go through json_decode. Not probed. |
| [adrienbrault/partial-json](https://packagist.org/packages/adrienbrault/partial-json) | — | 3,459 † | unresolved | Incomplete-JSON parser; not inspected. |
| [tdt/json](https://packagist.org/packages/tdt/json) | — | 1,987 † | unresolved | JSON stream reader; not inspected. |
| [hiroto-k/json5-php](https://packagist.org/packages/hiroto-k/json5-php) | — | 433 † | unresolved | JSON5 parser; valid-JSON route not inspected. |

Queries: `json`, `json parser`, `json decoder`, `json decode`, `json streaming parser` (03:23 UTC); limit 100 each; 429 hits, 314 unique. Supplemental queries `json stream`, `json5`, `jsonc`, `json lexer`, `json tokenizer`, `json reader`, `hjson`, `json pull parser` (15:19 UTC); limit 100 each; 547 hits, 373 unique, 238 not in the first pass; 976 hits and 552 unique overall. Packagist matches `json5`, `jsonc` and `hjson` loosely, so their first 100 hits are mostly generic JSON packages. † Download value from the supplemental snapshot; the package was not among the first-pass hits.
