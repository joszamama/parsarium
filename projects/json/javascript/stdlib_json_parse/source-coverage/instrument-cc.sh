#!/bin/sh
# Compiler wrapper for the Node.js source build. Only V8's JSON parser translation unit
# (deps/v8/src/json/json-parser.cc) gets Clang source-based coverage; every link step that
# writes an output adds the profile runtime so the instrumented object can be linked.
case "$(basename "$0")" in
  cc) real=clang-20 ;;
  c++) real=clang++-20 ;;
  *) echo "instrument-cc.sh: unknown wrapper name $0" >&2; exit 2 ;;
esac
compile=0 output=0 parser=0
for arg in "$@"; do
  case "$arg" in
    -c) compile=1 ;;
    -o) output=1 ;;
    */deps/v8/src/json/json-parser.cc) parser=1 ;;
  esac
done
if [ "$compile" = 1 ]; then
  [ "$parser" = 1 ] && exec "$real" "$@" -fprofile-instr-generate -fcoverage-mapping
  exec "$real" "$@"
fi
[ "$output" = 1 ] && exec "$real" "$@" -fprofile-instr-generate
exec "$real" "$@"
