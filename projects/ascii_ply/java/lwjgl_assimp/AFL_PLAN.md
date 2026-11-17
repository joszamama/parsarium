# AFL++ integration plan — lwjgl-assimp / ASCII PLY

Not implemented. Nothing under `fuzzing/afl-native/` or `fuzzing/afl-bridge/` was added or changed, and no campaign was run.

## Why the generic Java bridge is not enough

`scripts/build_afl_bridge.py` builds Java overlays around `java_trace.py`, which maps JaCoCo-covered lines of `PARSARIUM_PARSER_JAR` into the AFL++ map (`java_parser_source_lines_to_afl_bitmap`). For this path that jar is `lwjgl-assimp-3.4.3.jar`: struct accessors and the `aiImportFile` call. Its lines barely depend on PLY content, so that overlay would be wrapper-only feedback and must not be described as Assimp parser feedback.

## Feedback sources

| Scope | Features | Proposed `feedback_kind` |
| --- | --- | --- |
| `native` (default) | executed LLVM regions and branch directions in `/work/source/code/AssetLib/Ply/`, prefixed `native:` | `llvm_native_parser_regions_to_afl_bitmap` (already used by the Python C-extension overlays) |
| `dual` | the above plus JaCoCo lines of `lwjgl-assimp-3.4.3.jar`, prefixed `java:` | new label, e.g. `java_wrapper_lines_and_llvm_native_parser_regions_to_afl_bitmap` |

The receipt should report native and Java feature counts separately even in `dual` mode. [`afl-plan/java_llvm_native_trace.py`](afl-plan/java_llvm_native_trace.py) is a draft of the trace. It follows `python_llvm_native_trace.py`:

1. run `JavaCase` → `GenericHarness.fuzzerTestOneInput` with `PARSARIUM_LWJGL_NATIVE_DIR=/work/native` and a per-case `LLVM_PROFILE_FILE=…/case-%p-%m.profraw` (`%m` separates the profile runtimes in `libassimp.so` and `libdraco.so`);
2. `llvm-profdata merge`, then `llvm-cov export /work/native/libassimp.so … /work/source/code/AssetLib/Ply`;
3. write one feature per covered region start and branch direction;
4. exit non-zero when the JVM did, so `afl_proxy` raises `SIGABRT`. Checked exceptions such as `aiImportFile` returning `NULL` are swallowed by `GenericHarness` and count as rejections.

## Overlay sketch

```dockerfile
FROM --platform=linux/arm64 parsarium/ascii_ply-java-lwjgl_assimp:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.09c-1ubuntu3 clang \
    && rm -rf /var/lib/apt/lists/*
COPY fuzzing/afl-bridge/afl_proxy.c /work/afl_proxy.c
COPY fuzzing/afl-bridge/JavaCase.java /work/JavaCase.java
COPY <promoted java_llvm_native_trace.py> /work/afl_java_llvm_native_trace.py
COPY fuzzing/afl-native/ascii_ply/java/lwjgl_assimp/afl_trace /work/afl_trace
ENV PARSARIUM_FEEDBACK_SCOPE=native
RUN mkdir /work/afl-java-classes && javac -d /work/afl-java-classes /work/JavaCase.java
RUN AFL_LLVM_INSTRUMENT=CLASSIC afl-clang-fast -O2 /work/afl_proxy.c -ldl -o /work/afl_proxy
ENTRYPOINT ["/work/afl_proxy"]
```

`afl_trace` would be `exec python3 /work/afl_java_llvm_native_trace.py "$1" "$2"`. The base image already has `llvm` 18, `python3`, `/work/native`, the JaCoCo jars and the trimmed PLY sources. The `afl++` package pin must be one Ubuntu 24.04 provides; `4.09c-1ubuntu3` is what the existing Temurin-based Java overlays use.

## Shared changes needed later

These belong to separate, reviewed changes:

- `scripts/build_afl_bridge.py`: a branch for Java projects whose manifest has `underlying_coverage_subject_prefix` and a native library, selecting this trace instead of `java_trace.py`;
- promote the draft into `fuzzing/afl-bridge/` once it has been reviewed;
- `scripts/audit_fuzzing.py` and `scripts/smoke_ecosystem_feedback.py`: accept the native/dual kind for a Java project and require a native feature count above zero;
- the fuzzing README table: a Java row whose feedback is native parser regions.

## Verification before any campaign

1. `python3 parsarium.py build ascii_ply java lwjgl_assimp` produces `verification.json` with `underlying_source_lines_covered > 0` and the stock-native control passing.
2. Overlay receipt: control feature count, two identical control runs, and a second **valid** PLY seed (for example `controls/ascii_ply/triangle-colour.ply`) whose native feature set differs. This follows the differential check in `data/afl-feedback-differential.json` and uses no malformed input.
3. `afl prepare` / `afl run --check` preflight only.

## Limits

- Every case starts a JVM and runs `llvm-profdata` and `llvm-cov`. Expect a few executions per second at most.
- A native crash kills the JVM before the profile runtime writes, so a crashing case contributes no native features. It is still reported as a crash.
- The native library has no ASan/UBSan. Memory errors that do not crash go unnoticed. A sanitizer build inside the JVM would need `LD_PRELOAD` of the ASan runtime. That is a separate design.
- Features come from a coverage rebuild, not from the published stripped `libassimp.so`. QEMU-mode binary edges on the stock library (as in `ascii_ply/python/open3d`) would be the alternative if feedback must come from the shipped bytes. That route has no source lines.
