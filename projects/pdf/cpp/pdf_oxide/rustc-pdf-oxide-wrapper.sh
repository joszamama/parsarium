#!/bin/sh
set -eu
compiler=$1
shift
previous=
for arg in "$@"; do
  if [ "$previous" = --crate-name ] && [ "$arg" = pdf_oxide ]; then
    exec "$compiler" "$@" \
      -C passes=sancov-module \
      -C llvm-args=-sanitizer-coverage-level=3 \
      -C llvm-args=-sanitizer-coverage-trace-pc-guard \
      -C llvm-args=-sanitizer-coverage-prune-blocks=0
  fi
  previous=$arg
done
exec "$compiler" "$@"
