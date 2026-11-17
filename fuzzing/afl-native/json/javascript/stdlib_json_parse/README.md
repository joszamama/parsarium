# Node JSON.parse AFL++ target (parser-only native coverage)

This overlay builds Node.js 26.10.0 from the official source tarball with the
same pins as the [source-line build](../../../../../projects/json/javascript/stdlib_json_parse/source-coverage/Dockerfile):
Ubuntu base digest, tarball sha256 `7b3a546d…0ba20c5`, Clang 20.1.8, and
`./configure --v8-enable-temporal-support --without-npm`. The compiler
wrapper [`afl-cc.sh`](afl-cc.sh) adds `-fsanitize-coverage=trace-pc-guard`
to `deps/v8/src/json/json-parser.cc` and nothing else. Every executable link
adds AFL++'s compiler runtime (`afl-compiler-rt.o` from `afl++`
4.33c-1.1ubuntu1). The Docker build fails unless:

- `json-parser.o` is the only object with a `__sancov_guards` section,
- no other object references a SanitizerCoverage callback,
- `node` defines `__afl_area_ptr` and the trace-pc-guard callbacks, and
- `node` has one guard section no larger than that object's.

So every AFL++ map entry comes from V8's JSON parser object. The resulting
`node` (sha256 `0e8d211b…fa06f00d`) differs from the pinned official binary
and from the source-line build. A second from-scratch build (`--no-cache`)
produced the same hash.

The AFL++ target is `/opt/node/bin/node /work/adapter.mjs @@`. That is the
project's adapter, checked by sha256: it reads one local file, decodes it
with a strict UTF-8 `TextDecoder`, and calls `JSON.parse`. Each case starts
a fresh node process through the AFL++ fork server. No gdb and no extra
container privileges are involved.

`afl-showmap` on the verification machine, each run in a fresh container:

| Run | Map entries |
| --- | --- |
| `node -e 0` | 0 |
| adapter read + strict UTF-8 decode, no `JSON.parse` | 0 |
| nested-object control, 3 runs | 216, identical maps and raw hit counts |
| nested-array control, 3 runs | 206, identical maps and raw hit counts, different from the object map |

The object map has 67 entries the array map lacks, and the array map has 57
the object map lacks. The node binary has 4,866 guards. The [receipt](verification.json) records
image IDs, the object/array-only entries, map hashes, and toolchain versions.
[plan-smoke.json](plan-smoke.json) records the `afl prepare` and
`afl run --check` preflight.

AFL++ map entries are not line counts. Each entry is a trace-pc-guard point
(roughly a basic-block edge after optimization) with a bucketed hit count.
The 865 and 756 lines in the project receipt come from a separate LLVM
source-coverage build and measure something else. Code inlined into
`json-parser.o` from headers counts. `JSON.parse` builtin glue outside that
object, string internalization elsewhere in V8, and the adapter's
`TextDecoder` step do not.

From the repository root:

```sh
python3 parsarium.py afl build json javascript stdlib_json_parse
python3 parsarium.py afl prepare json javascript stdlib_json_parse runs/node-json-afl \
  --seed controls/json/nested-array.json
python3 parsarium.py afl run runs/node-json-afl --check
```

The first `afl build` compiles all of Node.js, which took about 21 minutes
on 12 cores. Later builds use the Docker cache. No fuzz campaign is part of
this verification.
