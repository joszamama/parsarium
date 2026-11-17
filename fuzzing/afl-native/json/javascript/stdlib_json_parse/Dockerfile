# AFL++ bitmap populated only from native V8 JsonParser function-entry names.
# The pinned Node runtime and gdb probe are verified by the base project receipt.
FROM --platform=linux/arm64 parsarium/json-javascript-stdlib_json_parse-native-feedback:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.21c-5 clang \
    && rm -rf /var/lib/apt/lists/*
COPY fuzzing/afl-bridge/afl_proxy.c /work/afl_proxy.c
COPY fuzzing/afl-native/json/javascript/stdlib_json_parse/afl_trace /work/afl_trace
RUN AFL_LLVM_INSTRUMENT=CLASSIC afl-clang-fast -O2 /work/afl_proxy.c -ldl -o /work/afl_proxy
ENTRYPOINT ["/work/afl_proxy"]
