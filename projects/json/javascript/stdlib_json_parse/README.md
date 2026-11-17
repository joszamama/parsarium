# JSON.parse — JSON / JavaScript (standard)

Node.js `26.10.0` (V8 `14.6.202.34-node.34`), pinned by image digest and node binary sha256. [Manifest](manifest.json) · [verification receipt](verification.json) · [standard API inventory](../../../../data/javascript/json/standard.json)

`JSON.parse` takes a string, not bytes. The adapter ([adapters/javascript/json_node.mjs](../../../../adapters/javascript/json_node.mjs), copied here as `adapter.mjs` and checked by sha256) decodes the input with `new TextDecoder('utf-8', {fatal: true})` and passes that string to `JSON.parse`. The UTF-8 step belongs to the adapter.

The build replays two valid controls: `controls/json/nested-object.json` (mounted) and `controls/json/nested-array.json` (copied into the image as `second-control.json`, same sha256).

## Feedback

`JSON.parse` is C++ inside the node binary. V8 source coverage of a replay lists 84 scripts and no JSON parser script, so there are no parser source lines to count.

The binary is unstripped, so `native-feedback-probe/run-smoke.sh` sets a one-shot gdb breakpoint on each of the 142 `v8::internal::JsonParser<...>` functions and records which ones run:

| Run | JsonParser functions entered |
| --- | --- |
| `node -e 0` baseline | 0 |
| nested-object control, twice | 21, identical sets |
| nested-array control | 23 (5 not in the control set, 3 missing from it) |

That is function-entry feedback. It is not source-line coverage, basic blocks, or edges, and it is not AFL++ feedback. Inlined code does not show up. The probe needs `SYS_PTRACE` and `seccomp=unconfined` in a separate image, and Debian's gdb package there is not hash-pinned (its version is in the receipt). No fuzz engine is wired to this path.

## Run from the repository root

```sh
python3 parsarium.py build json javascript stdlib_json_parse
python3 parsarium.py run json javascript stdlib_json_parse controls/json/nested-object.json
python3 parsarium.py run json javascript stdlib_json_parse controls/json/nested-array.json
```

`build` replays both controls and runs the native feedback probe.
