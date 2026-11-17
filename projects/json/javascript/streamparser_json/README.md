# @streamparser/json — JSON / JavaScript

`@streamparser/json` 0.0.26 is MIT licensed and pinned by the [npm release archive](source-lock.json). The adapter passes a local `Buffer` to the documented [`JSONParser.write(input)`](https://www.npmjs.com/package/@streamparser/json?activeTab=readme) API, receives completed values via `onValue`, and summarizes the root JSON structure. It does not call `JSON.parse` on input.

The adapter writes the entire local Buffer in one call, then calls `end()` if needed. With the default undefined separator, `src/tokenparser.ts` ends after one root value; `src/tokenizer.ts` continues over the remainder of the Buffer in its `ENDED` state and accepts only JSON whitespace. This is one complete JSON document, limited to the two valid nested-object and nested-array controls tested here. The package implements its own tokenizer and token parser, separate from `stream-json` and `bfj`.

```sh
python3 parsarium.py build json javascript streamparser_json
python3 parsarium.py run json javascript streamparser_json controls/json/nested-object.json
python3 parsarium.py afl build json javascript streamparser_json
python3 parsarium.py afl prepare json javascript streamparser_json runs/streamparser-json-afl
python3 parsarium.py afl run runs/streamparser-json-afl --check
```

V8 coverage counts executed `@streamparser/json` package source lines. The AFL++ bridge maps parser source ranges into feedback. Repeated runs of the two valid controls have stable, distinct maps. This is a launcher and feedback check, not a fuzzing campaign.
