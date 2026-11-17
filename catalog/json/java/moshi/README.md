# Moshi — JSON / Java

**Verified package/API path in an incomplete format cell.**

- **Pinned release:** `com.squareup.moshi:moshi:1.15.2` (Apache-2.0)
- **Parser family:** Moshi's own `JsonReader` and `JsonUtf8Reader`; Okio supplies I/O
- **Local input API:** `JsonReader.of(BufferedSource).readJsonValue()` over Okio's local file source
- **Documentation:** [pinned release source](https://repo.maven.apache.org/maven2/com/squareup/moshi/moshi/1.15.2/moshi-1.15.2-sources.jar), `main/com/squareup/moshi/JsonReader.java` lines 205 and 489
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json)
- **Evidence:** [parser record](../../../../data/java/json/parsers.json), [control results](../../../../data/java/json/verification.json), [project and commands](../../../../projects/json/java/moshi/README.md)

The controls produced the expected nested structures. JaCoCo covered 306 pinned Moshi parser source lines; repeated feedback was stable and differed on the second valid structure. Okio and Kotlin runtime dependencies are pinned and recorded separately from the parser family.
