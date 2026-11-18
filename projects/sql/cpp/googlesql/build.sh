#!/bin/sh
set -eu
src=/work/googlesql
# Harness package inside the //googlesql/... visibility group (//googlesql/parser is implementation-visible).
mkdir -p "$src/googlesql/parsarium"
cp /work/harness.cc /work/parser-probe.cc /work/fuzzer.cc "$src/googlesql/parsarium/"
cp /work/BUILD.parsarium "$src/googlesql/parsarium/BUILD"
cd "$src"
# --ignore_dev_dependency drops upstream's dev-only hermetic LLVM toolchain, so Bazel's autodetected
# toolchain uses the compiler named below. Plain link libraries: the default as-needed wrapping drops
# libstdc++ from ICU's rules_foreign_cc tool links.
bazel_build() {
  bazel --output_user_root=/work/bazel-root build --ignore_dev_dependency -c opt --dynamic_mode=off \
    --repo_env=CC=clang --repo_env=CXX=clang++ --repo_env=BAZEL_LINKLIBS=-lstdc++:-lm \
    --jobs="$(nproc)" --show_result=0 --noshow_progress "$@" > /work/bazel-build.log 2>&1 \
    || { tail -80 /work/bazel-build.log; exit 1; }
}
bin=bazel-out/aarch64-opt/bin

if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only googlesql/parser sources (tokenizer, Textmapper lexer and parser,
  # lookahead transformer, AST nodes) are instrumented; abseil, protobuf, ICU and the harness are not.
  bazel_build --action_env=AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt \
    //googlesql/parsarium:replay //googlesql/parsarium:parser-probe
  out=$(readlink -f "$bin")
  for object in $(find "$out" -name '*.o' | sort); do
    if nm "$object" 2>/dev/null | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "${object#$out/}"; fi
  done > /work/afl-instrumented-objects.txt
  test -s /work/afl-instrumented-objects.txt
  if grep -v '^googlesql/parser/' /work/afl-instrumented-objects.txt; then echo 'unexpected AFL++ objects' >&2; exit 1; fi
  cp "$bin/googlesql/parsarium/replay" "$bin/googlesql/parsarium/parser-probe" /work/
  cp /work/parser-probe /work/fuzzer
else
  # Coverage build: LLVM source coverage on googlesql/parser only. Generated Textmapper and AST files
  # are mapped from bazel-out next to the hand-written parser sources under one prefix.
  cov='-fprofile-instr-generate,-fcoverage-mapping,-fcoverage-compilation-dir=/work/googlesql'
  cov="$cov,-fcoverage-prefix-map=$bin/googlesql/parser=googlesql/parser"
  bazel_build --per_file_copt="googlesql/parser/.*@$cov" --linkopt=-fprofile-instr-generate \
    //googlesql/parsarium:replay //googlesql/parsarium:parser-probe //googlesql/parsarium:fuzzer
  cp "$bin/googlesql/parsarium/replay" "$bin/googlesql/parsarium/parser-probe" \
    "$bin/googlesql/parsarium/fuzzer" /work/
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
# Generated parser sources next to the hand-written ones, for coverage source views.
for file in "$bin"/googlesql/parser/*.cc "$bin"/googlesql/parser/*.h; do
  test -e "$src/googlesql/parser/$(basename "$file")" || cp "$file" "$src/googlesql/parser/"
done
bazel --output_user_root=/work/bazel-root shutdown
