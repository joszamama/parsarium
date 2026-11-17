# jackson-core — JSON / Java

Pinned release: `2.23.0` (Apache-2.0). [Manifest](manifest.json) · [source lock](source-lock.json) · [container receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/json/java/jackson_core/verification.json)

This adapter opens a local file as an `InputStream`, passes it to `JsonFactory.createParser(InputStream)`, and consumes the `JsonParser.nextToken()` stream. It reports counts, depth, values, and root fields/items. The source JAR documents the input overload; the release POM documents the license. Jackson Core is also the tokenizer beneath the selected `jackson-databind` path: these are two package/API routes in one parser family, not two engines. Field-name canonicalization is disabled because the default uses a wall-clock-seeded symbol table and makes repeated coverage differ.

The nested-object control produces five objects, three arrays, maximum depth four, and the expected scalar values. The second valid nested-array control produces two objects, four arrays, maximum depth three, and five top-level items. The container recorded 442 Jackson Core source lines, and repeat probes produced identical parser features and AFL++ maps. The two valid structures differed by 109 parser features and 109 AFL++ tuples. These controls establish the stated subset, not full format conformance.

## Run from the repository root

```sh
python3 parsarium.py build json java jackson_core
python3 parsarium.py run json java jackson_core controls/json/nested-object.json
python3 parsarium.py run json java jackson_core controls/json/nested-array.json
python3 parsarium.py afl build json java jackson_core
python3 parsarium.py afl prepare json java jackson_core runs/json-jackson_core-afl
python3 parsarium.py afl run runs/json-jackson_core-afl --check
```

The AFL++ preparation command only creates a seeded run directory. It does not start a campaign.
