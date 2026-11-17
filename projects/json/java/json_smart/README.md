# json-smart — JSON / Java

Pinned release: `net.minidev:json-smart:2.6.1` (Apache-2.0), with pinned `accessors-smart:2.6.1` and ASM `9.11.1` runtime dependencies. [Manifest](manifest.json) · [source lock](source-lock.json) · [container receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/json/java/json_smart/verification.json)

The adapter passes local UTF-8 bytes to `JSONParser(MODE_RFC4627).parse(byte[])`. That documented mode accepts top-level JSON objects and arrays and trailing whitespace, matching the two valid controls. Its own `JSONParserByteArray`, `JSONParserBase`, and `JSONParserMemory` classes perform the parse; the dependencies provide object access and bytecode support rather than JSON tokenization.

The nested-object control produced the expected structure and covered 261 pinned parser source lines. The nested-array control produced the expected separate structure. Repeated control feedback was identical; the array changed 16 parser features and 16 AFL++ tuples. These controls establish only this tested JSON subset.

## Run from the repository root

```sh
python3 parsarium.py build json java json_smart
python3 parsarium.py run json java json_smart controls/json/nested-object.json
python3 parsarium.py run json java json_smart controls/json/nested-array.json
python3 parsarium.py afl build json java json_smart
python3 parsarium.py afl prepare json java json_smart runs/json-json_smart-afl
python3 parsarium.py afl run runs/json-json_smart-afl --check
```

The AFL++ preparation creates a seeded run directory and does not start a campaign.
