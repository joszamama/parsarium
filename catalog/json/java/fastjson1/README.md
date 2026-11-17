# fastjson 1.x — JSON / Java

**Pilot / incomplete format cell.** This path is verified on two valid nested controls.

- **Release:** `com.alibaba:fastjson:1.2.83`
- **License:** Apache-2.0 ([release POM](https://repo.maven.apache.org/maven2/com/alibaba/fastjson/1.2.83/fastjson-1.2.83.pom), pinned SHA256 in [source lock](../../../../projects/json/java/fastjson1/source-lock.json))
- **API:** `JSON.parse(byte[])` over bytes read from a local file. [Release source](https://repo.maven.apache.org/maven2/com/alibaba/fastjson/1.2.83/fastjson-1.2.83-sources.jar).
- **Family:** fastjson 1.x `DefaultJSONParser` / `JSONLexer`; separate from fastjson2 and the fastjson 2.x facade.
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json).
- **Evidence:** [parser record](../../../../data/java/json/parsers.json), [control receipt](../../../../projects/json/java/fastjson1/verification.json), [AFL feedback](../../../../data/java/json/afl-feedback.json).

The primary deps.dev metric sums all releases of `com.alibaba:fastjson`, including 2.x facade releases; it is package-coordinate adoption, not 1.x-only adoption or JSON-specific use. The 1.2.83 release has the highest single-release dependent count in that snapshot (1,494).

```sh
python3 parsarium.py build json java fastjson1
python3 parsarium.py run json java fastjson1 controls/json/nested-object.json
python3 parsarium.py afl build json java fastjson1
python3 parsarium.py afl prepare json java fastjson1 runs/json-fastjson1-afl
```
