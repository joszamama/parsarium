# fastjson2 — JSON / Java

**Verified package/API path in an incomplete format cell.**

- **Pinned release:** `com.alibaba.fastjson2:fastjson2:2.0.66` (Apache-2.0)
- **Parser family:** fastjson2's own JSONReader implementation
- **Local input API:** `JSON.parse(byte[])` on bytes read from a local file
- **Documentation:** [pinned release source](https://repo.maven.apache.org/maven2/com/alibaba/fastjson2/fastjson2/2.0.66/fastjson2-2.0.66-sources.jar), `JSON.java` around line 251
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json)
- **Evidence:** [parser record](../../../../data/java/json/parsers.json), [control results](../../../../data/java/json/verification.json), [project and commands](../../../../projects/json/java/fastjson2/README.md)

The controls produced the expected nested structures. JaCoCo covered 560 pinned `JSONReader` source lines; repeated parser feedback was stable and differed on the second valid structure. The 2.x `com.alibaba:fastjson` coordinate is a compatibility facade in the same parser family and remains unverified as a separate API path.
