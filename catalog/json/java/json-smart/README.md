# json-smart — JSON / Java

**Verified package/API path in an incomplete format cell.**

- **Pinned release:** `net.minidev:json-smart:2.6.1` (Apache-2.0)
- **Parser family:** json-smart's own byte and base parsers
- **Local input API:** `JSONParser(MODE_RFC4627).parse(byte[])` on local UTF-8 bytes
- **Documentation:** [pinned release source](https://repo.maven.apache.org/maven2/net/minidev/json-smart/2.6.1/json-smart-2.6.1-sources.jar), `JSONParser.java` lines 149–165 and 245–248
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json)
- **Evidence:** [parser record](../../../../data/java/json/parsers.json), [control results](../../../../data/java/json/verification.json), [project and commands](../../../../projects/json/java/json_smart/README.md)

Both controls produced the expected structures. JaCoCo covered 261 pinned parser source lines; repeated parser feedback was stable and differed on the second valid structure. The selected mode and controls establish only this tested JSON subset.
