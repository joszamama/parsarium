# JAVA × JSON: selected parsers (pilot)

2 control-verified third-party paths selected. The ceiling is ten; this pilot builds the two highest-adoption general-purpose parser leads from independent parser families and does not pad the selection. jackson-core (80,053) ranks between them but is the tokenizer jackson-databind drives, so it stays a same-family lead. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)). A dependent is counted once per release it depends on. The default-release count alone is skewed by release age: json-simple 1.1.1 (2012, the only real release) shows 1,163 while jackson-databind 2.23.0 shows 367. The single-release maximum is recorded as a cross-check; both summed and maximum rank jackson-databind first and gson second among the selected paths.

| Rank | Package | Release | Metric | Max single release | Parsed scope | Parser family |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | [jackson-databind](https://javadoc.io/static/com.fasterxml.jackson.core/jackson-databind/2.23.0/com/fasterxml/jackson/databind/ObjectMapper.html) | 2.23.0 | 162,890 | 4,098 (2.18.2) | RFC 8259 JSON text into untyped Map/List | Jackson (jackson-core streaming parser + databind untyped mapping) |
| 2 | [gson](https://javadoc.io/doc/com.google.code.gson/gson/2.15.0/com.google.gson/com/google/gson/Gson.html) | 2.15.0 | 33,240 | 3,828 (2.10.1) | RFC 8259 JSON text into untyped Map/List | Gson (com.google.gson.stream.JsonReader + ObjectTypeAdapter untyped mapping) |

The Jackson adapter disables `CANONICALIZE_FIELD_NAMES` so repeated runs produce identical parser coverage. Gson runs `new Gson().fromJson(Reader, Object.class)` with default settings and its own `JsonReader`; it shares no code with Jackson. See the [parser records](parsers.json).

## Standard API (none)

OpenJDK 25.0.5 exports no JSON parsing package from any module. JSON-P / JSON-B are Jakarta EE specifications, not Java SE; their implementations are logged as leads. Details in [standard.json](standard.json).

## Lead log

Numeric leads looked up on deps.dev, not verified and not selected. Maven Central text search ranks by relevance, so the search hits alone do not surface adoption.

| Lead | Version seen | Summed direct dependents | Max single release | Status |
| --- | --- | ---: | ---: | --- |
| [com.fasterxml.jackson.core:jackson-core](https://central.sonatype.com/artifact/com.fasterxml.jackson.core/jackson-core) | 2.23.0 | 80,053 | 1,934 | JsonFactory.createParser(File) streaming tokenizer. It is the tokenizer the selected jackson-databind path drives, so it is the same parser family; not run as a separate path. |
| [com.alibaba:fastjson](https://central.sonatype.com/artifact/com.alibaba/fastjson) | 2.0.66 | 10,021 | 1,494 | fastjson 2.x artifact is a compatibility facade over fastjson2; JSON.parse(byte[]) control not run. |
| [org.json:json](https://central.sonatype.com/artifact/org.json/json) | 20260814 | 6,923 | 564 | new JSONObject(JSONTokener(Reader)) over its own tokenizer; control not run. |
| [com.alibaba.fastjson2:fastjson2](https://central.sonatype.com/artifact/com.alibaba.fastjson2/fastjson2) | 2.0.66.android8 | 2,973 | 180 | JSON.parse(byte[]) with its own JSONReader; deps.dev default release is an android8 variant. Control not run. |
| [com.googlecode.json-simple:json-simple](https://central.sonatype.com/artifact/com.googlecode.json-simple/json-simple) | 1.1.1 | 1,557 | 1,163 | JSONParser.parse(Reader) with a JFlex lexer; single 2012 release. Highest default-release count only because of version-age bias. Control not run. |
| [net.minidev:json-smart](https://central.sonatype.com/artifact/net.minidev/json-smart) | 2.6.1 | 1,542 | 220 | JSONParser.parse(byte[]/Reader); control not run. |
| [com.squareup.moshi:moshi](https://central.sonatype.com/artifact/com.squareup.moshi/moshi) | 1.15.2 | 1,097 | 166 | JsonReader.of(BufferedSource) over Okio; control not run. |
| [org.eclipse.parsson:parsson](https://central.sonatype.com/artifact/org.eclipse.parsson/parsson) | 1.1.9 | 495 | 122 | Jakarta JSON-P implementation, Json.createReader(InputStream); control not run. |
| [com.eclipsesource.minimal-json:minimal-json](https://central.sonatype.com/artifact/com.eclipsesource.minimal-json/minimal-json) | 0.9.5 | 338 | 225 | Json.parse(Reader); control not run. |
| [org.glassfish:jakarta.json](https://central.sonatype.com/artifact/org.glassfish/jakarta.json) | 2.0.1 | 336 | 171 | GlassFish JSON-P 2.0 implementation preceding parsson; control not run. |
| [com.jsoniter:jsoniter](https://central.sonatype.com/artifact/com.jsoniter/jsoniter) | 0.9.23 | 79 | 55 | JsonIterator.deserialize(byte[]); dynamic codegen modes; control not run. |

Queries: `json`, `json parser`, `json databind`, `json-p`, `gson`; limit 100 each; 322 hits, 322 unique.
