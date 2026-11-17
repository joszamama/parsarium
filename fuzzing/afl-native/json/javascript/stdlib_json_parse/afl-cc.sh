#!/bin/sh
# Compiler wrapper for the AFL++ Node.js source build. Only V8's JSON parser translation unit
# (deps/v8/src/json/json-parser.cc) gets SanitizerCoverage trace-pc-guard, the LLVM-native
# instrumentation AFL++'s compiler runtime consumes; every executable link adds that runtime.
case "$(basename "$0")" in
  cc) real=clang-20 ;;
  c++) real=clang++-20 ;;
  *) echo "afl-cc.sh: unknown wrapper name $0" >&2; exit 2 ;;
esac
compile=0 output=0 parser=0 shared=0
for arg in "$@"; do
  case "$arg" in
    -c) compile=1 ;;
    -o) output=1 ;;
    -shared) shared=1 ;;
    */deps/v8/src/json/json-parser.cc) parser=1 ;;
  esac
done
if [ "$compile" = 1 ]; then
  [ "$parser" = 1 ] && exec "$real" "$@" -fsanitize-coverage=trace-pc-guard
  exec "$real" "$@"
fi
[ "$output" = 1 ] && [ "$shared" = 0 ] && exec "$real" "$@" /usr/lib/afl/afl-compiler-rt.o
exec "$real" "$@"
