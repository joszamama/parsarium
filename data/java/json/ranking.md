# JAVA × JSON: selected parsers (pilot)

8 control-verified third-party package/API paths selected. The ceiling is ten; this pilot ranks verified paths and does not pad the selection. jackson-core (80,053) is the tokenizer jackson-databind (162,890) drives; their separate direct and mapping APIs belong to the same parser family. Gson (33,240), org.json (6,923), fastjson2 (2,973), json-simple (1,557), json-smart (1,542), and Moshi (1,097) are independent parser families. Higher-metric unresolved leads remain visible below.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)). A dependent is counted once per release it depends on. The default-release count alone is skewed by release age: json-simple 1.1.1 (2012) shows 1,163 while jackson-databind 2.23.0 shows 367. The single-release maximum is a cross-check; summed counts rank the eight selected package paths as shown. Package adoption is not JSON-specific use.

| Rank | Package | Release | Metric | Max single release | Parsed scope | Parser family |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | [jackson-databind](https://javadoc.io/static/com.fasterxml.jackson.core/jackson-databind/2.23.0/com/fasterxml/jackson/databind/ObjectMapper.html) | 2.23.0 | 162,890 | 4,098 (2.18.2) | RFC 8259 JSON text into untyped Map/List | Jackson (jackson-core streaming parser + databind untyped mapping) |
| 2 | [jackson-core](https://javadoc.io/static/com.fasterxml.jackson.core/jackson-core/2.23.0/com/fasterxml/jackson/core/JsonFactory.html) | 2.23.0 | 80,053 | 1,934 (2.18.2) | RFC 8259 JSON text from local InputStream into streaming tokens | Jackson (same tokenizer driven by jackson-databind) |
| 3 | [gson](https://javadoc.io/doc/com.google.code.gson/gson/2.15.0/com.google.gson/com/google/gson/Gson.html) | 2.15.0 | 33,240 | 3,828 (2.10.1) | RFC 8259 JSON text into untyped Map/List | Gson (com.google.gson.stream.JsonReader + ObjectTypeAdapter untyped mapping) |
| 4 | [org.json:json](https://github.com/stleary/JSON-java) | 20260814 | 6,923 | 564 (20231013) | Valid nested JSON from local Reader into JSONObject/JSONArray | org.json JSONTokener plus object/array builders |
| 5 | [fastjson2](https://github.com/alibaba/fastjson2/blob/main/README.md) | 2.0.66 | 2,973 | 180 (2.0.60) | RFC 8259 JSON text from local UTF-8 bytes into object/array values | fastjson2 JSONReaderUTF8/ASCII |
| 6 | [json-simple](https://javadoc.io/static/com.googlecode.json-simple/json-simple/1.1.1/org/json/simple/parser/JSONParser.html) | 1.1.1 | 1,557 | 1,163 (1.1.1) | Valid nested JSON from local UTF-8 Reader into JSONObject/JSONArray | JSONParser plus generated JFlex Yylex |
| 7 | [json-smart](https://github.com/netplex/json-smart-v2) | 2.6.1 | 1,542 | 220 (2.3) | Valid nested RFC 4627 JSON object/array from local UTF-8 bytes | json-smart JSONParserByteArray/Base |
| 8 | [moshi](https://github.com/square/moshi) | 1.15.2 | 1,097 | 166 (1.15.2) | Valid nested JSON from local Okio BufferedSource into untyped values | Moshi JsonReader/JsonUtf8Reader |

The two Jackson adapters disable `CANONICALIZE_FIELD_NAMES` so repeated runs produce identical parser coverage. The direct jackson-core path covered 442 parser source lines, had stable control feedback, and differed by 109 parser features and 109 AFL++ tuples on the valid nested-array control. Gson runs `new Gson().fromJson(Reader, Object.class)` with default settings and its own `JsonReader`; it shares no code with Jackson. The org.json adapter uses `JSONTokener(Reader)` in strict mode and consumes one complete root; its control covered 252 parser source lines, and the valid array changed 10 parser features and 10 AFL tuples. Fastjson2 runs `JSON.parse(byte[])` through its own JSONReader classes; its pinned control covered 560 parser source lines, with a stable repeated control and 137 parser features and AFL++ tuples differing on the valid nested-array control. Json-smart runs `JSONParser(MODE_RFC4627).parse(byte[])` through its own parser classes; its control covered 261 source lines, with a stable repeat and 16 parser features and AFL tuples changing on the valid array. Json-simple runs `JSONParser.parse(Reader)` through its generated JFlex lexer; the 2012 release covered 247 parser source lines, with stable repeated control and 21 parser features and AFL tuples changing on the valid array. Moshi runs `JsonReader.of(BufferedSource).readJsonValue()` through its own JsonUtf8Reader, while Okio supplies the local stream. Its control covered 306 own parser lines, and 12 features and 12 tuples changed on the valid array. See the [parser records](parsers.json).

## Standard API (none)

OpenJDK 25.0.5 exports no JSON parsing package from any module. JSON-P / JSON-B are Jakarta EE specifications, not Java SE; their implementations are logged as leads. Details in [standard.json](standard.json).

## Lead log

Numeric leads looked up on deps.dev, not verified and not selected. jackson-core, org.json, fastjson2, json-simple, json-smart, and Moshi were promoted from this log after their direct paths passed the control and feedback gates. Maven Central text search ranks by relevance, so the search hits alone do not surface adoption.

| Lead | Version seen | Summed direct dependents | Max single release | Status |
| --- | --- | ---: | ---: | --- |
| [com.alibaba:fastjson](https://central.sonatype.com/artifact/com.alibaba/fastjson) | 2.0.66 | 10,021 | 1,494 | fastjson 2.x compatibility facade over the selected fastjson2 engine; its own API path is not control-verified. The summed metric also includes fastjson 1.x releases, which used a different engine. |
| [com.googlecode.json-simple:json-simple](https://central.sonatype.com/artifact/com.googlecode.json-simple/json-simple) | 1.1.1 | 1,557 | 1,163 | Promoted to verified: JSONParser.parse(Reader) with its own JFlex lexer; 2012 release with age-skewed default-release count. |
| [org.eclipse.parsson:parsson](https://central.sonatype.com/artifact/org.eclipse.parsson/parsson) | 1.1.9 | 495 | 122 | Jakarta JSON-P implementation, Json.createReader(InputStream); control not run. |
| [com.eclipsesource.minimal-json:minimal-json](https://central.sonatype.com/artifact/com.eclipsesource.minimal-json/minimal-json) | 0.9.5 | 338 | 225 | Json.parse(Reader); control not run. |
| [org.glassfish:jakarta.json](https://central.sonatype.com/artifact/org.glassfish/jakarta.json) | 2.0.1 | 336 | 171 | GlassFish JSON-P 2.0 implementation preceding parsson; control not run. |
| [com.jsoniter:jsoniter](https://central.sonatype.com/artifact/com.jsoniter/jsoniter) | 0.9.23 | 79 | 55 | JsonIterator.deserialize(byte[]); dynamic codegen modes; control not run. |

The deps.dev default version for fastjson2 is `2.0.66.android8`; this Java SE harness pins the ordinary `2.0.66` release. The 2,973 metric sums the package coordinate’s releases and is not a release-specific download count.

Queries: `json`, `json parser`, `json databind`, `json-p`, `gson`; limit 100 each; 322 hits, 322 unique.
