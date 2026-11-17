# org.json:json — JSON / Java

**Verified package/API path in an incomplete format cell.**

- **Pinned release:** `org.json:json:20260814` (Public Domain in its release POM)
- **Parser family:** org.json's own JSONTokener, JSONObject, and JSONArray
- **Local input API:** `JSONTokener(Reader).nextValue()` over a local UTF-8 file stream, followed by `nextClean()` for document completion
- **Documentation:** [pinned release source](https://repo.maven.apache.org/maven2/org/json/json/20260814/json-20260814-sources.jar), `JSONTokener.java` lines 43, 321, and 455
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json)
- **Evidence:** [parser record](../../../../data/java/json/parsers.json), [control results](../../../../data/java/json/verification.json), [project and commands](../../../../projects/json/java/orgjson/README.md)

The two controls produced the expected nested structures. JaCoCo covered 252 pinned parser source lines; repeated parser feedback was stable and differed on the second valid structure. This release is public domain; older pre-20220924 JSON-java releases had different terms.
