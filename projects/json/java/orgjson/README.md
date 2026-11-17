# org.json:json — JSON / Java

Pinned release: `org.json:json:20260814` (Public Domain, as declared in the release POM). [Manifest](manifest.json) · [source lock](source-lock.json) · [container receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/json/java/orgjson/verification.json)

The adapter passes a local UTF-8 `Reader` to `JSONTokener`, calls `nextValue()`, and checks `nextClean() == 0` after the root. It uses `JSONParserConfiguration.withStrictMode()` and converts parsed `JSONObject`/`JSONArray` nodes to untyped maps/lists for an observable structural summary. The pinned release implements its own tokenizer and object/array builders. The public-domain declaration applies to this release; the older historical JSON License is not the license recorded for it.

The valid nested-object control produced the expected summary and covered 252 pinned source lines in `JSONTokener`, `JSONObject`, `JSONArray`, and parser configuration. The valid nested-array control produced the expected separate summary. Repeated control feedback was identical, and the array changed 10 parser features and 10 AFL++ tuples. These controls establish only the tested JSON subset.

## Run from the repository root

```sh
python3 parsarium.py build json java orgjson
python3 parsarium.py run json java orgjson controls/json/nested-object.json
python3 parsarium.py run json java orgjson controls/json/nested-array.json
python3 parsarium.py afl build json java orgjson
python3 parsarium.py afl prepare json java orgjson runs/json-orgjson-afl
python3 parsarium.py afl run runs/json-orgjson-afl --check
```

The AFL++ preparation creates a seeded run directory and does not start a campaign.
