# json-simple — JSON / Java

Pinned release: `com.googlecode.json-simple:json-simple:1.1.1` (Apache-2.0, published 2012). [Manifest](manifest.json) · [source lock](source-lock.json) · [container receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/json/java/json_simple/verification.json)

The adapter passes a local UTF-8 `Reader` to `JSONParser.parse(Reader)`. The pinned parser uses its generated JFlex `Yylex` lexer and returns JSONObject/JSONArray values; its parser state consumes an EOF token after the root. The old POM lists JUnit without test scope, but the verified container runs this parse path using only the release jar.

The nested-object control produced the expected structural summary and covered 247 pinned source lines: 146 in `Yylex`, 95 in `JSONParser`, and six in `Yytoken`. The valid nested-array control produced the expected separate summary. Repeated control feedback was identical; the array changed 21 parser features and 21 AFL++ tuples. These controls establish only the tested JSON subset.

## Run from the repository root

```sh
python3 parsarium.py build json java json_simple
python3 parsarium.py run json java json_simple controls/json/nested-object.json
python3 parsarium.py run json java json_simple controls/json/nested-array.json
python3 parsarium.py afl build json java json_simple
python3 parsarium.py afl prepare json java json_simple runs/json-json_simple-afl
python3 parsarium.py afl run runs/json-json_simple-afl --check
```

The AFL++ preparation creates a seeded run directory and does not start a campaign.
