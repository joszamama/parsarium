#!/bin/sh
set -eu
# LibUCW's own Perl configure, static libraries only: libucw (fastbufs, mempools), libucw-charset
# (ucw-xml's input decoding) and libucw-xml. No shared libraries, Perl modules, utilities or docs.
cd /work/source
# Its 2015 configure requires ucw/default.cfg by a relative path, which current Perl no longer finds through '.'.
export PERL5LIB=/work/source
# Its CPU detection knows i386 and amd64 only; on aarch64 the documented CPU_xxx variables are set by hand
# (64-bit pointers, little endian, 8-byte struct alignment, no unaligned-access shortcut).
cpu=''
if [ "$(uname -m)" = aarch64 ]; then cpu='CPU_64BIT_POINTERS=1 CPU_LITTLE_ENDIAN=1 CPU_STRUCT_ALIGN=8'; fi
./configure CC=clang "CEXTRA=-fprofile-instr-generate -fcoverage-mapping" "LEXTRA=-fprofile-instr-generate" \
  -CONFIG_SHARED -CONFIG_DEBUG -CONFIG_UCW_PERL -CONFIG_UCW_PERL_MODULES -CONFIG_UCW_SHELL_UTILS -CONFIG_UCW_UTILS -CONFIG_DOC \
  -CONFIG_UCW_THREADS $cpu
# Only the three static libraries are needed. The tree's test and utility programs (ucw-cs2cs, json-test, ...)
# fail to link with the current toolchain's static-library ordering, so make continues past them (-k) and
# the libraries are checked explicitly.
make -k -j 4 > /work/make.log 2>&1 || true
libs='/work/source/obj/ucw-xml/libucw-xml-6.5.a /work/source/obj/charset/libucw-charset-6.5.a /work/source/obj/ucw/libucw-6.5.a'
for lib in $libs; do test -f "$lib"; done
common='-O1 -g -fno-omit-frame-pointer -I/work/source -I/work/source/obj'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c $libs -lm -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c $libs -lm -o /work/fuzzer
