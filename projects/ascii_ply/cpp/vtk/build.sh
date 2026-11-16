#!/bin/sh
set -eu

# Build the minimal static VTK module closure of VTK::IOPLY with plain
# compiler flags, then recompile the IO/PLY reader and its bundled vtkPLY
# parser with coverage and sanitizer instrumentation, using the include and
# define flags CMake recorded for those two files.
src=/work/source
build=/work/vtk-build
cc=clang
cxx=clang++
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'

cmake -S $src -B $build -G 'Unix Makefiles' \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=$cc -DCMAKE_CXX_COMPILER=$cxx \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_SHARED_LIBS=OFF \
  -DVTK_BUILD_TESTING=OFF -DVTK_BUILD_EXAMPLES=OFF -DVTK_BUILD_DOCUMENTATION=OFF \
  -DVTK_ENABLE_WRAPPING=OFF -DVTK_WRAP_PYTHON=OFF -DVTK_WRAP_JAVA=OFF \
  -DVTK_ENABLE_REMOTE_MODULES=OFF -DVTK_BUILD_ALL_MODULES=OFF \
  -DVTK_GROUP_ENABLE_Imaging=DONT_WANT -DVTK_GROUP_ENABLE_MPI=DONT_WANT \
  -DVTK_GROUP_ENABLE_Qt=DONT_WANT -DVTK_GROUP_ENABLE_Rendering=DONT_WANT \
  -DVTK_GROUP_ENABLE_StandAlone=DONT_WANT -DVTK_GROUP_ENABLE_Views=DONT_WANT \
  -DVTK_GROUP_ENABLE_Web=DONT_WANT -DVTK_SMP_IMPLEMENTATION_TYPE=Sequential \
  -DVTK_SMP_ENABLE_STDTHREAD=OFF -DVTK_MODULE_ENABLE_VTK_IOPLY=YES
cmake --build $build --target vtkIOPLY -j 4

ply_flags=$(python3 - "$build/compile_commands.json" "$src/IO/PLY/vtkPLY.cxx" <<'PY'
import json
import shlex
import sys

entries = json.load(open(sys.argv[1]))
entry, = [e for e in entries if e["file"] == sys.argv[2]]
args = entry.get("arguments") or shlex.split(entry["command"])
keep = []
i = 1
while i < len(args):
    arg = args[i]
    if arg == "-isystem":
        keep += [arg, args[i + 1]]
        i += 1
    elif arg.startswith(("-I", "-D", "-std=")) and arg != "-DNDEBUG":
        keep.append(arg)
    i += 1
print(" ".join(shlex.quote(arg) for arg in keep))
PY
)
test -n "$ply_flags"

mkdir -p /work/obj
for file in $src/IO/PLY/vtkPLY.cxx $src/IO/PLY/vtkPLYReader.cxx /work/harness.cpp; do
  eval "$cxx $common -DNDEBUG $ply_flags -I/work -c $file -o /work/obj/$(basename "$file" | sed 's/\.[^.]*$//').o"
done
$cxx -std=c++17 $common -I/work -c /work/replay.cpp -o /work/obj/replay.o
$cxx -std=c++17 $common -I/work -c /work/fuzz.cpp -o /work/obj/fuzz.o

# The instrumented objects replace libvtkIOPLY; every other archive in the
# module closure is linked as one group to resolve VTK's internal ordering.
libs=$(ls $build/lib/libvtk*.a | grep -v '/libvtkIOPLY-')
objects='/work/obj/vtkPLY.o /work/obj/vtkPLYReader.o /work/obj/harness.o'
$cxx -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined $objects /work/obj/replay.o \
  -Wl,--start-group $libs -Wl,--end-group -lpthread -ldl -lm -o /work/replay
$cxx -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined $objects /work/obj/fuzz.o \
  -Wl,--start-group $libs -Wl,--end-group -lpthread -ldl -lm -o /work/fuzzer
