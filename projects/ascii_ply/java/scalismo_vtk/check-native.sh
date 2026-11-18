#!/bin/sh
set -eu

# ABI checks and the instrumented impl jar for the libvtkIOPLY-9.1.so built by build-vtk.sh.
built=$(find /work/vtk/build -name 'libvtkIOPLY-9.1.so.1' | head -1)
mkdir -p /work/native-cov /work/native-stock
cp -L "$built" /work/native-cov/libvtkIOPLY-9.1.so
unzip -q -j /work/lib/vtkjavanativeslinuximpl-0.2-RC1.jar \
  'ch/unibas/cs/gravis/vtkjavanativelibs/impl/*.so' -d /work/native-stock
soname() { readelf -d "$1" | sed -n 's/.*(SONAME).*\[\(.*\)\]/\1/p'; }
test "$(soname /work/native-cov/libvtkIOPLY-9.1.so)" = "$(soname /work/native-stock/libvtkIOPLY-9.1.so)"
nm /work/native-cov/libvtkIOPLY-9.1.so | grep -q __llvm_profile_runtime

# Every symbol the stock JNI wrapper libvtkIOPLYJava.so takes from the stock libvtkIOPLY is
# exported by the rebuilt library (inline template instances that GCC emitted out of line are
# not part of that interface), and every VTK symbol the rebuilt library imports is defined by
# the stock VTK libraries it is loaded with.
exports() { nm -D --defined-only "$1" | awk '{print $3}' | sed 's/@.*//' | sort -u; }
exports /work/native-stock/libvtkIOPLY-9.1.so > /work/abi-stock-exports.txt
exports /work/native-cov/libvtkIOPLY-9.1.so > /work/abi-built-exports.txt
nm -D --undefined-only /work/native-stock/libvtkIOPLYJava.so | awk '{print $2}' | sed 's/@.*//' \
  | sort -u | comm -12 - /work/abi-stock-exports.txt > /work/abi-jni-uses.txt
test -s /work/abi-jni-uses.txt
missing=$(comm -23 /work/abi-jni-uses.txt /work/abi-built-exports.txt)
if [ -n "$missing" ]; then
  echo "rebuilt libvtkIOPLY lacks symbols the stock JNI wrapper uses: $missing" >&2
  exit 1
fi
nm -D --undefined-only /work/native-cov/libvtkIOPLY-9.1.so | awk '{print $2}' | sed 's/@.*//' \
  | grep 'vtk' | sort -u > /work/abi-built-vtk-imports.txt
for lib in IOCore CommonExecutionModel CommonDataModel CommonMisc CommonCore sys; do
  exports "/work/native-stock/libvtk$lib-9.1.so"
done | sort -u > /work/abi-stock-dependency-exports.txt
unresolved=$(comm -23 /work/abi-built-vtk-imports.txt /work/abi-stock-dependency-exports.txt)
if [ -n "$unresolved" ]; then
  echo "rebuilt libvtkIOPLY imports symbols the stock VTK libraries lack: $unresolved" >&2
  exit 1
fi
printf '{"jni_wrapper_symbols_from_ioply": %s, "built_vtk_imports": %s, "missing": 0, "unresolved": 0}\n' \
  "$(wc -l < /work/abi-jni-uses.txt)" "$(wc -l < /work/abi-built-vtk-imports.txt)" > /work/abi-check.json

# Instrumented copy of the impl jar: the same entries with only libvtkIOPLY-9.1.so replaced.
mkdir -p /work/impl-cov/ch/unibas/cs/gravis/vtkjavanativelibs/impl /work/lib-cov
cp /work/lib/vtkjavanativeslinuximpl-0.2-RC1.jar /work/lib-cov/vtkjavanativeslinuximpl-0.2-RC1.jar
cp /work/native-cov/libvtkIOPLY-9.1.so /work/impl-cov/ch/unibas/cs/gravis/vtkjavanativelibs/impl/
(cd /work/impl-cov && zip -q -0 /work/lib-cov/vtkjavanativeslinuximpl-0.2-RC1.jar \
  ch/unibas/cs/gravis/vtkjavanativelibs/impl/libvtkIOPLY-9.1.so)
rm -rf /work/native-stock
