# json-simple — JSON / Java

**Verified package/API path in an incomplete format cell.**

- **Pinned release:** `com.googlecode.json-simple:json-simple:1.1.1` (Apache-2.0)
- **Parser family:** JSONParser with its generated JFlex Yylex lexer
- **Local input API:** `JSONParser.parse(Reader)` over a local UTF-8 file stream
- **Documentation:** [release API reference](https://javadoc.io/static/com.googlecode.json-simple/json-simple/1.1.1/org/json/simple/parser/JSONParser.html)
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json)
- **Evidence:** [parser record](../../../../data/java/json/parsers.json), [control results](../../../../data/java/json/verification.json), [project and commands](../../../../projects/json/java/json_simple/README.md)

Both controls produced the expected nested structures. JaCoCo covered 247 pinned parser/lexer source lines; repeated parser feedback was stable and differed on the second valid structure. The 2012 release has a high default-release dependent count partly because it remains the default; the within-cell ranking uses the same summed deps.dev metric as other selected Java packages.
