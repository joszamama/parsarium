#!/bin/sh
# Compiler used for fltk-sys's CMake build (and every other cc-crate build).
# Instrumentation flags are added only to translation units from the vendored
# cfltk C shim and FLTK library sources, so CMake probes, libFuzzer, and other
# build-script code stay uninstrumented. Invoked as native-cc or native-c++.
case "$0" in
  *++) real="$PARSARIUM_REAL_CXX" ;;
  *) real="$PARSARIUM_REAL_CC" ;;
esac
for arg in "$@"; do
  case "$arg" in
    */fltk-sys-1.5.23/cfltk/src/*|*/fltk-sys-1.5.23/cfltk/fltk/src/*)
      # shellcheck disable=SC2086
      exec "$real" $PARSARIUM_NATIVE_FLAGS "$@" ;;
  esac
done
exec "$real" "$@"
