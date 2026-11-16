#!/bin/sh
set -eu

# Compile the Easy3D util/core/fileio sources that SurfaceMeshIO links against,
# plus bundled RPly, directly. Easy3D's CMake rewrites util/version.h with the
# configure date, so the pinned tree is built without it.
src=/work/source
defs='-DNDEBUG -DELPP_FEATURE_ALL -DELPP_STL_LOGGING -DELPP_THREAD_SAFE
  -DELPP_NO_DEFAULT_LOG_FILE -DELPP_DISABLE_DEFAULT_CRASH_HANDLING
  -DEasy3D_VERSION_MAJOR=2 -DEasy3D_VERSION_MINOR=6 -DEasy3D_VERSION_PATCH=1
  -DEasy3D_VERSION_STRING="2.6.1" -DEasy3D_VERSION_NUMBER=1020601
  -DEasy3D_RESOURCE_DIR="/work/source/resources"'
cxx_sources="$src/easy3d/util/console_style.cpp $src/easy3d/util/file_system.cpp
  $src/easy3d/util/logging.cpp $src/easy3d/util/progress.cpp
  $src/easy3d/util/stop_watch.cpp $src/easy3d/util/string.cpp
  $src/easy3d/core/surface_mesh.cpp $src/easy3d/core/surface_mesh_builder.cpp
  $src/easy3d/core/model.cpp
  $src/easy3d/fileio/ply_reader_writer.cpp $src/easy3d/fileio/translator.cpp
  $src/easy3d/fileio/surface_mesh_io.cpp $src/easy3d/fileio/surface_mesh_io_ply.cpp
  $src/easy3d/fileio/surface_mesh_io_obj.cpp $src/easy3d/fileio/surface_mesh_io_off.cpp
  $src/easy3d/fileio/surface_mesh_io_stl.cpp $src/easy3d/fileio/surface_mesh_io_sm.cpp
  $src/easy3d/fileio/surface_mesh_io_geojson.cpp"

build() {
  out=$1
  shift
  mkdir -p /work/obj-$out
  clang -O1 -g -fno-omit-frame-pointer "$@" -I$src -c $src/3rd_party/rply/rply.c \
    -o /work/obj-$out/rply.o
  objects=/work/obj-$out/rply.o
  for file in $cxx_sources /work/harness.cpp; do
    object=/work/obj-$out/$(basename "$file" .cpp).o
    clang++ -std=c++17 -O1 -g -fno-omit-frame-pointer $defs "$@" -I$src -I/work \
      -c "$file" -o "$object"
    objects="$objects $object"
  done
  echo "$objects"
}

replay_objects=$(build replay -fprofile-instr-generate -fcoverage-mapping)
clang++ -fprofile-instr-generate $replay_objects /work/replay.cpp -I/work \
  -lpthread -o /work/replay
fuzz_objects=$(build fuzzer -fsanitize=fuzzer-no-link,address,undefined)
clang++ -fsanitize=fuzzer,address,undefined $fuzz_objects /work/fuzz.cpp -I/work \
  -lpthread -o /work/fuzzer
