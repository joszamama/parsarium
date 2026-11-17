# PHP × JSON: selected parsers (pilot)

5 control-verified third-party paths selected. The ceiling is ten; this pilot does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

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

Composer depends on seld/jsonlint, which inflates the download count. Composer calls `json_decode` first and uses `JsonParser` to report errors. Laminas is abandoned; its default API route calls ext/json, so this adapter explicitly enables its own PHP Decoder. JSON Machine has an independent streaming parser for member boundaries, but the selected decoder delegates each member value to PHP ext/json. salsify decodes strings, escapes and numbers in its own code; the adapter supplies a listener that builds objects and lists, and rejects input that does not end exactly one document. pcrov/jsonreader has its own pull lexer and state machine; both valid controls match an independent type-tagged JSON tree, and its parser-only AFL bridge changes three source features and three tuples between them.

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

Queries: `json`, `json parser`, `json decoder`, `json decode`, `json streaming parser`; limit 100 each; 429 hits, 314 unique.
