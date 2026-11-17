# bfj — JSON / JavaScript

`bfj` 9.1.4 is MIT licensed and pinned by its [npm release archive](source-lock.json). The adapter passes a local `Buffer` through `Readable.from([bytes])` to the documented [`bfj.parse(stream, options)`](https://www.npmjs.com/package/bfj?activeTab=readme) API. It summarizes the returned JSON value; the adapter does not call `JSON.parse` on the input.

The default `{ ndjson: false }` path in bfj's `src/walk.js` parses one value, then reads to end of stream and emits a data error for trailing non-whitespace. `src/parse.js` rejects that error. The valid nested-object and nested-array controls produce the expected structural summaries. This establishes the tested JSON subset only.

```sh
python3 parsarium.py build json javascript bfj
python3 parsarium.py run json javascript bfj controls/json/nested-object.json
python3 parsarium.py afl build json javascript bfj
python3 parsarium.py afl prepare json javascript bfj runs/bfj-afl
python3 parsarium.py afl run runs/bfj-afl --check
```

V8 coverage counts executed `bfj` package source lines. The AFL++ bridge maps bfj parser source ranges into AFL feedback. The two valid controls are used only to check that repeat runs are stable and distinct; no fuzzing campaign is part of this receipt.
