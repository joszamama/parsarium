# Moshi — JSON / Java

Pinned release: `com.squareup.moshi:moshi:1.15.2` (Apache-2.0). The pinned Okio `3.7.0` dependency supplies the local byte stream; Kotlin runtime jars and transitive annotations are pinned in the [source lock](source-lock.json). [Manifest](manifest.json) · [container receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/json/java/moshi/verification.json)

The adapter opens a local file with Okio, passes its `BufferedSource` to `JsonReader.of`, calls `readJsonValue()`, and checks for `END_DOCUMENT`. Moshi's own `JsonUtf8Reader` tokenizes the JSON. Okio is an I/O dependency, not a second parser. The reader uses its default non-lenient mode.

The nested-object control produced the expected structural summary and covered 306 pinned Moshi source lines in `JsonUtf8Reader` and `JsonReader`. The valid nested-array control produced the expected separate summary. Repeated control feedback was identical; the array changed 12 parser features and 12 AFL++ tuples. These controls establish only the tested JSON subset.

## Run from the repository root

```sh
python3 parsarium.py build json java moshi
python3 parsarium.py run json java moshi controls/json/nested-object.json
python3 parsarium.py run json java moshi controls/json/nested-array.json
python3 parsarium.py afl build json java moshi
python3 parsarium.py afl prepare json java moshi runs/json-moshi-afl
python3 parsarium.py afl run runs/json-moshi-afl --check
```

The AFL++ preparation creates a seeded run directory and does not start a campaign.
