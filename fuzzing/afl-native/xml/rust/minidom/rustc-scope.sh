#!/bin/bash
# RUSTC_WRAPPER: keep cargo-afl SanitizerCoverage flags only for crates in AFL_SCOPE_CRATES.
rustc=$1; shift
log=${AFL_SCOPE_LOG:-/work/sancov-scope.log}
crate=; prev=
for arg in "$@"; do [ "$prev" = --crate-name ] && crate=$arg; prev=$arg; done
case " $AFL_SCOPE_CRATES " in *" $crate "*)
    echo "instrumented $crate" >> "$log"; exec "$rustc" "$@";; esac
args=(); held=
for arg in "$@"; do
    if [ -n "$held" ]; then
        case "$arg" in passes=sancov*|llvm-args=-sanitizer-coverage*) ;; *) args+=(-C "$arg");; esac
        held=; continue
    fi
    case "$arg" in
        -C) held=1;;
        -Cpasses=sancov*|-Cllvm-args=-sanitizer-coverage*) ;;
        *) args+=("$arg");;
    esac
done
[ -n "$crate" ] && [ "$crate" != ___ ] && echo "uninstrumented $crate" >> "$log"
exec "$rustc" "${args[@]}"
