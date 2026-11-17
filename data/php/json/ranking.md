# PHP × JSON: selected parsers (pilot)

1 control-verified third-party path selected. The ceiling is ten; this pilot builds only the highest-adoption package with its own JSON parser and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

PHP code mostly parses JSON with the bundled `json_decode` (ext/json). The most downloaded Packagist JSON helpers wrap it, so they are excluded from the third-party ranking rather than counted as separate parsers.

## Primary within-cell adoption metric

Packagist total downloads, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [seld/jsonlint](https://packagist.org/packages/seld/jsonlint) | 1.12.2 | 252,371,311 | RFC 8259 JSON text into stdClass/array/scalars | seld/jsonlint Lexer and LR table parser |

Composer depends on seld/jsonlint, which inflates the download count. Composer calls `json_decode` first and uses `JsonParser` to report errors.

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [json_decode](https://www.php.net/manual/en/function.json-decode.php) | PHP 8.5.12 | PHP ext/json re2c scanner and Bison parser |

## Lead log

Numeric leads from the same snapshot, not verified and not selected. JWT, JSON Schema, JSONPath, JMESPath, serializer, and JSON-RPC hits were not treated as parser leads.

| Lead | Version seen | Packagist downloads | Status | Note |
| --- | --- | ---: | --- | --- |
| [laminas/laminas-json](https://packagist.org/packages/laminas/laminas-json) | 3.8.0 | 35,102,503 | unresolved | Json::decode calls json_decode by default; a separate pure-PHP Laminas\Json\Decoder runs only when Json::$useBuiltinEncoderDecoder is true. Packagist marks the package abandoned. That own-decoder path and control were not run in this pilot. |
| [colinodell/json5](https://packagist.org/packages/colinodell/json5) | v3.0.0 | 32,796,867 | unresolved | JSON5 superset decoder Json5Decoder::decode(string). Project documentation describes trying json_decode first for performance, so valid RFC 8259 input may route to ext/json; own-parser path not run. |
| [halaxa/json-machine](https://packagist.org/packages/halaxa/json-machine) | 1.2.6 | 30,443,415 | unresolved | Pull parser Items::fromString/fromFile/fromStream with its own Lexer and Parser; the default ExtJsonDecoder decodes items with json_decode. Parser-family split and control not run. |
| [zendframework/zend-json](https://packagist.org/packages/zendframework/zend-json) | 3.1.2 | 24,719,945 | unresolved | Abandoned predecessor of laminas/laminas-json; same decoder lineage. Not run. |
| [salsify/json-streaming-parser](https://packagist.org/packages/salsify/json-streaming-parser) | v8.3.1 | 7,715,575 | unresolved | Own pure-PHP streaming Parser over a stream resource with a listener API; control not run in this pilot. |
| [pcrov/jsonreader](https://packagist.org/packages/pcrov/jsonreader) | 1.0.4 | 1,520,757 | unresolved | Pull reader JsonReader::json/open with its own lexer; control not run in this pilot. |
| [cerbero/json-parser](https://packagist.org/packages/cerbero/json-parser) | 1.1.1 | 823,332 | unresolved | Lazy JsonParser over strings, streams and files with its own tokenizer; value decoding path and control not run. |
| [nette/utils](https://packagist.org/packages/nette/utils) | v4.1.6 | 514,679,287 | excluded | Nette\Utils\Json::decode is a json_decode wrapper; shares the verified ext/json family. |
| [symfony/serializer](https://packagist.org/packages/symfony/serializer) | v8.2.0-BETA2 | 384,296,452 | excluded | JsonDecode encoder calls json_decode; shares the verified ext/json family. |
| [beste/json](https://packagist.org/packages/beste/json) | 1.8.0 | 36,059,399 | excluded | Json::decode helper over json_decode; shares the verified ext/json family. |
| [ergebnis/json](https://packagist.org/packages/ergebnis/json) | 1.7.0 | 33,479,596 | excluded | Json value object validated through json_decode; shares the verified ext/json family. |

Queries: `json`, `json parser`, `json decoder`, `json decode`, `json streaming parser`; limit 100 each; 429 hits, 314 unique.
