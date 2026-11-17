FROM --platform=linux/arm64 parsarium/ascii_ply-java-f3d:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.09c-1ubuntu3 clang \
    && rm -rf /var/lib/apt/lists/*
COPY fuzzing/afl-bridge/afl_proxy.c /work/afl_proxy.c
COPY fuzzing/afl-bridge/JavaCase.java /work/JavaCase.java
COPY fuzzing/afl-native/ascii_ply/java/f3d/native_trace.py /work/native_trace.py
COPY fuzzing/afl-native/ascii_ply/java/f3d/afl_trace /work/afl_trace
RUN mkdir -p /work/afl-java-classes \
    && javac -d /work/afl-java-classes /work/JavaCase.java \
    && AFL_LLVM_INSTRUMENT=CLASSIC afl-clang-fast -O2 /work/afl_proxy.c -ldl -o /work/afl_proxy \
    && chmod +x /work/afl_trace
ENTRYPOINT ["/work/afl_proxy"]
