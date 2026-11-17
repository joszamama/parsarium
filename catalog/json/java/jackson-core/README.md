# jackson-core — JSON / Java

**Verified package/API path in an incomplete format cell.**

- **Pinned release:** `com.fasterxml.jackson.core:jackson-core:2.23.0` (Apache-2.0)
- **Parser family:** Jackson; shares the tokenizer used by selected `jackson-databind`
- **Local input API:** `JsonFactory.createParser(InputStream)` over a local file stream, then `JsonParser.nextToken()`
- **Documentation:** [release API reference](https://javadoc.io/static/com.fasterxml.jackson.core/jackson-core/2.23.0/com/fasterxml/jackson/core/JsonFactory.html)
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json)
- **Evidence:** [parser record](../../../../data/java/json/parsers.json), [control result](../../../../data/java/json/verification.json), [project and commands](../../../../projects/json/java/jackson_core/README.md)

The adapter consumes the direct Jackson Core token stream and reports structure. On the nested-object control it observed five objects, three arrays, maximum depth four, and seven top-level keys. On the nested-array control it observed two objects, four arrays, maximum depth three, and five top-level items. JaCoCo covered 442 parser source lines; repeated control feedback was stable and differed from the second valid structure. This establishes only the tested subset.
