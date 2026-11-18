#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
# Upstream's documented BSDBuild route (INSTALL.md): configure, make depend all, make install.
# Static Agar-Core, Agar-GUI (no display driver is opened), Agar-Math and Agar-SG, the
# libraries SG_ObjectLoadPLY(3) needs; the optional AU, MAP, NET, SK and VG libraries are off.
cd /work/source
CC=clang CFLAGS="$common" ./configure --prefix=/work/agar --disable-shared \
  --enable-gui --enable-math --enable-sg --disable-net --disable-sk --disable-vg \
  --disable-au --disable-map --disable-nls --with-gl --with-glu \
  --without-freetype --without-fontconfig --without-x --without-sdl --without-sdl2
make depend all
make install
cd /work

includes="$(/work/agar/bin/agar-sg-config --cflags)"
libs="/work/agar/lib/libag_sg.a /work/agar/lib/libag_math.a /work/agar/lib/libag_gui.a /work/agar/lib/libag_core.a -lGLU -lGL -lm -ldl -pthread"
clang -std=c11 $common $includes -c /work/harness.c -o /work/harness.o
clang -std=c11 $common -c /work/replay.c -o /work/replay.o
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o \
  $libs -o /work/replay

clang -std=c11 $common -c /work/fuzz.c -o /work/fuzz.o
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o \
  $libs -o /work/fuzzer
