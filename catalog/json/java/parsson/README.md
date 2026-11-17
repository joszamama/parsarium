# Parsson — JSON / Java

**Pilot / incomplete format cell.** This path is verified on two valid nested controls.

- **Pinned release:** `org.eclipse.parsson:parsson:1.1.9` plus `jakarta.json:jakarta.json-api:2.1.3`.
- **License:** EPL-2.0 in the [parent release POM](https://repo.maven.apache.org/maven2/org/eclipse/parsson/project/1.1.9/project-1.1.9.pom) and release JAR; source headers also offer GPL-2.0 with Classpath Exception. [Hashes](../../../../projects/json/java/parsson/source-lock.json).
- **Local API:** `new JsonProviderImpl().createParser(InputStream)` followed by `next()`, `getValue()`, and `hasNext()` through EOF. [Provider source](https://repo.maven.apache.org/maven2/org/eclipse/parsson/parsson/1.1.9/parsson-1.1.9-sources.jar).
- **Family:** Parsson `JsonParserImpl` and `JsonTokenizer`; `jakarta.json-api` supplies interfaces, not another parser engine.
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json).
- **Evidence:** [parser record](../../../../data/java/json/parsers.json), [control receipt](../../../../projects/json/java/parsson/verification.json), [AFL feedback](../../../../data/java/json/afl-feedback.json).

The object control produced 5 objects, 3 arrays, a maximum depth of 4, seven top-level keys, and the expected scalar values. JaCoCo covered 512 Parsson source lines. The array control produced 2 objects and 4 arrays; repeated parser feedback was stable, and 19 parser features and 19 AFL++ tuples changed. The two controls do not establish complete grammar coverage.

The deps.dev metric (495 summed direct dependents) measures adoption of this Maven coordinate across releases, including JSON-P use that may not call `JsonProviderImpl` directly.

```sh
python3 parsarium.py build json java parsson
python3 parsarium.py run json java parsson controls/json/nested-object.json
python3 parsarium.py afl build json java parsson
python3 parsarium.py afl prepare json java parsson runs/json-parsson-afl
```
