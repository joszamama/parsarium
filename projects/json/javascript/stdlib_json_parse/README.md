# JSON.parse — JSON / JavaScript (standard)

Node.js `26.10.0` (V8 `14.6.202.34-node.34`), pinned by image digest and node binary sha256. [Manifest](manifest.json) · [verification receipt](verification.json) · [standard API inventory](../../../../data/javascript/json/standard.json)

`JSON.parse` takes a string, not bytes. The adapter ([adapters/javascript/json_node.mjs](../../../../adapters/javascript/json_node.mjs), copied here as `adapter.mjs` and checked by sha256) decodes the input with `new TextDecoder('utf-8', {fatal: true})` and passes that string to `JSON.parse`. The UTF-8 step belongs to the adapter.

The build replays two valid controls: `controls/json/nested-object.json` (mounted) and `controls/json/nested-array.json` (copied into the image as `second-control.json`, same sha256).

## Feedback

`JSON.parse` is C++ inside the node binary. V8 source coverage of a replay lists 84 scripts and no JSON parser script, so the pinned binary itself gives no parser source lines.

### V8 parser source lines (source-built Node.js)

[`source-coverage/`](source-coverage/) builds Node.js 26.10.0 from the official source tarball (`node-v26.10.0.tar.xz`, sha256 `7b3a546d…0ba20c5`). That tarball and the linux-arm64 tarball whose `bin/node` is byte-identical to the pinned binary are both listed in the release's signed `SHASUMS256.txt.asc` (key `5BE8A3F6C8A5C01D106C0AD820B1A390B168D356`). The build uses Clang 20.1.8 (official linux-arm64 releases use Clang 20.1) and the same Temporal setting. A compiler wrapper adds `-fprofile-instr-generate -fcoverage-mapping` to `deps/v8/src/json/json-parser.cc` and nothing else. The build fails unless `json-parser.o` is the only object with a coverage section.

The adapter, both controls, and the expected summaries are unchanged. Each run writes its own LLVM profile:

| Run | json-parser.cc + .h lines | Functions |
| --- | --- | --- |
| `node -e 0` | 0 | 0 |
| adapter read + strict UTF-8 decode, no `JSON.parse` | 0 | 0 |
| nested-object control, twice | 865 (768 + 97), identical per-line counts | 102 |
| nested-array control, twice | 756 (659 + 97), identical per-line counts | 94 |

The object control covers 147 lines the array control misses; the array control covers 38 the object control misses. Out of 2,046 instrumented lines, 1,860 are in `json-parser.cc` and 186 in `json-parser.h`. The receipt records image IDs, source hashes, and the line lists.

These counts come from the source-built binary (sha256 `6d9e19d9…20767645`), not the pinned official one. Builtin glue outside the parser and the adapter's `TextDecoder` step are not counted. They are replay line counts, not AFL++ edges. The first build compiles all of Node.js, which took about 25 minutes on 12 cores. Later builds use the Docker cache.

### Function entries (pinned binary)

The binary is unstripped, so `native-feedback-probe/run-smoke.sh` sets a one-shot gdb breakpoint on each of the 142 `v8::internal::JsonParser<...>` functions and records which ones run:

| Run | JsonParser functions entered |
| --- | --- |
| `node -e 0` baseline | 0 |
| nested-object control, twice | 21, identical sets |
| nested-array control | 23 (5 not in the control set, 3 missing from it) |

That is function-entry feedback. It is not source-line coverage, basic blocks, or edges. Inlined code does not show up. The probe needs `SYS_PTRACE` and `seccomp=unconfined` in a separate image, and Debian's gdb package there is not hash-pinned (its version is in the receipt). A [separate AFL++ bridge](../../../../fuzzing/afl-native/json/javascript/stdlib_json_parse/README.md) hashes these function names into a feedback bitmap. Its tuples are not V8 parser edges, so this standard path stays staged for fuzzing.

## Run from the repository root

```sh
python3 parsarium.py build json javascript stdlib_json_parse
python3 parsarium.py run json javascript stdlib_json_parse controls/json/nested-object.json
python3 parsarium.py run json javascript stdlib_json_parse controls/json/nested-array.json
```

`build` replays both controls, runs the gdb function-entry probe, and runs the source-coverage measurement. On its own:

```sh
projects/json/javascript/stdlib_json_parse/source-coverage/run-smoke.sh
```
