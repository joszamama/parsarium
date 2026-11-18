#!/bin/sh
set -eu

# Rebuild libvtkIOPLY-9.1.so from the VTK 9.1.0 release with LLVM coverage. The stock
# vtkjavanativeslinuximpl 0.2-RC1 jar carries the jzy3d VTK 9.1 Java wrapper build (GCC 9.3,
# shared libraries, soname libvtkIOPLY-9.1.so.1). Only libvtkIOPLY-9.1.so is swapped; every
# other native library, including libvtkIOPLYJava.so and the VTK core it links, stays stock.
coverage='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
cmake -S /work/vtk/source -B /work/vtk/build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$coverage" -DCMAKE_CXX_FLAGS="$coverage" \
  -DCMAKE_C_FLAGS_RELEASE='-DNDEBUG' -DCMAKE_CXX_FLAGS_RELEASE='-DNDEBUG' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DBUILD_SHARED_LIBS=ON -DVTK_BUILD_TESTING=OFF -DVTK_BUILD_EXAMPLES=OFF \
  -DVTK_BUILD_DOCUMENTATION=OFF -DVTK_ENABLE_WRAPPING=OFF -DVTK_WRAP_PYTHON=OFF \
  -DVTK_WRAP_JAVA=OFF -DVTK_ENABLE_REMOTE_MODULES=OFF -DVTK_BUILD_ALL_MODULES=OFF \
  -DVTK_GROUP_ENABLE_Imaging=DONT_WANT -DVTK_GROUP_ENABLE_MPI=DONT_WANT \
  -DVTK_GROUP_ENABLE_Qt=DONT_WANT -DVTK_GROUP_ENABLE_Rendering=DONT_WANT \
  -DVTK_GROUP_ENABLE_StandAlone=DONT_WANT -DVTK_GROUP_ENABLE_Views=DONT_WANT \
  -DVTK_GROUP_ENABLE_Web=DONT_WANT -DVTK_MODULE_ENABLE_VTK_IOPLY=YES
cmake --build /work/vtk/build --target IOPLY -j "$(nproc)"
