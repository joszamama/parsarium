#!/bin/sh
set -eu

tk_config=$(dpkg -L tcl8.6-dev | grep '/tclConfig.sh$' | head -1)
if [ -z "$tk_config" ]; then echo 'tclConfig.sh unavailable' >&2; exit 1; fi
cd /work/tk/unix
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
  LDFLAGS='-fprofile-instr-generate' \
  ./configure --prefix=/opt/tk --with-tcl="$(dirname "$tk_config")" --enable-shared \
  || { tail -80 config.log; exit 1; }
make -j 4
make install

cd /work/python
CC=clang TCLTK_CFLAGS='-I/opt/tk/include -I/usr/include/tcl8.6' \
  TCLTK_LIBS='-L/opt/tk/lib -ltk8.6 -ltcl8.6' \
  ./configure --prefix=/opt/python --enable-shared --with-ensurepip=no
make -j 4
make install
LD_LIBRARY_PATH=/opt/tk/lib:/opt/python/lib /opt/python/bin/python3.13 \
  -c 'import _tkinter, tkinter; print(_tkinter.TK_VERSION, tkinter.TkVersion)'
