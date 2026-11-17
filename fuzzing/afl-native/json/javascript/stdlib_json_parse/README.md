# Node JSON.parse AFL++ function-entry bridge

This overlay feeds AFL++ a bitmap made from **native V8 `JsonParser` function
entries**. The pinned Node 26.10.0 binary exposes 142 `v8::internal::JsonParser`
text symbols. A one-shot gdb probe records the symbols entered while
`JSON.parse` reads one local valid JSON file. The AFL bridge hashes those names
into its map. Bridge instrumentation also adds tuples; the reported tuple count
is not a count of V8 control-flow edges or source lines.

For the two valid controls, the no-parser baseline yielded 13 bitmap tuples;
the object control yielded 41 in two identical runs, and the valid array
variant yielded 43 with a different map. Direct symbol probes observed 0, 21,
and 23 `JsonParser` functions respectively. The base project verifies the
different parsed JSON summaries. [Verification](verification.json) records
image IDs, hashes, function differences, and map hashes.

From the repository root:

```sh
python3 parsarium.py afl build json javascript stdlib_json_parse
python3 parsarium.py afl prepare json javascript stdlib_json_parse runs/node-json-afl \
  --seed controls/json/nested-array.json --timeout-ms 30000
python3 parsarium.py afl run runs/node-json-afl --check
```

The generated Docker command needs `SYS_PTRACE` and
`seccomp=unconfined` for gdb. Each case launches a fresh debugger and Node
process. Two six-case valid-control `afl-showmap` measurements on the
verification machine took roughly 0.9–1.5 seconds per case (about 0.65–1.14
cases per second); the latest exact measurement is in the receipt. Actual
campaign throughput is unmeasured and depends on the host. The
bridge records function-entry sets only; inlined parser code is invisible.
No fuzz campaign is part of this verification.
