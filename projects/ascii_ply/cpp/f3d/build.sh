#!/bin/sh
set -eu

# Build a static, headless VTK with the modules F3D 4.0.1 requires, swap
# coverage- and sanitizer-instrumented vtkPLY and vtkPLYReader objects into
# libvtkIOPLY, then build F3D with its static native plugin through the
# harness CMake project. That project instruments only the native plugin
# targets, which hold the F3D PLY reader path.
vtk_src=/work/vtk/source
vtk_build=/work/vtk/build
f3d_src=/work/f3d/source
f3d_build=/work/f3d/build
cc=clang
cxx=clang++
jobs=${PARSARIUM_JOBS:-4}
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
link='-fprofile-instr-generate -fcoverage-mapping -fsanitize=address,undefined'
fuzz_link='-fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer,address,undefined'

modules=''
for module in CommonColor CommonCore CommonDataModel CommonExecutionModel \
    CommonSystem FiltersGeneral FiltersGeometry IOCityGML IOGeometry IOImage \
    IOImport IOLegacy IOPLY IOXML IOXMLParser ImagingCore ImagingHybrid \
    InteractionStyle InteractionWidgets RenderingAnnotation RenderingCore \
    RenderingGridAxes RenderingOpenGL2 RenderingVolumeOpenGL2 TestingCore; do
  modules="$modules -DVTK_MODULE_ENABLE_VTK_$module=YES"
done

# X11, Wayland and EGL are off: F3D's engine::createNone never opens a
# window, and VTK keeps only its dlopen-based OSMesa headless backend.
cmake -S $vtk_src -B $vtk_build -G 'Unix Makefiles' \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=$cc -DCMAKE_CXX_COMPILER=$cxx \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_SHARED_LIBS=OFF \
  -DVTK_BUILD_TESTING=OFF -DVTK_BUILD_EXAMPLES=OFF -DVTK_BUILD_DOCUMENTATION=OFF \
  -DVTK_ENABLE_WRAPPING=OFF -DVTK_WRAP_PYTHON=OFF -DVTK_WRAP_JAVA=OFF \
  -DVTK_ENABLE_REMOTE_MODULES=OFF -DVTK_BUILD_ALL_MODULES=OFF \
  -DVTK_GROUP_ENABLE_Imaging=DONT_WANT -DVTK_GROUP_ENABLE_MPI=DONT_WANT \
  -DVTK_GROUP_ENABLE_Qt=DONT_WANT -DVTK_GROUP_ENABLE_Rendering=DONT_WANT \
  -DVTK_GROUP_ENABLE_StandAlone=DONT_WANT -DVTK_GROUP_ENABLE_Views=DONT_WANT \
  -DVTK_GROUP_ENABLE_Web=DONT_WANT -DVTK_SMP_IMPLEMENTATION_TYPE=Sequential \
  -DVTK_SMP_ENABLE_STDTHREAD=OFF -DVTK_USE_X=OFF -DVTK_USE_Wayland=OFF \
  -DVTK_OPENGL_HAS_EGL=OFF $modules
cmake --build $vtk_build -j "$jobs"

ply_flags=$(python3 - "$vtk_build/compile_commands.json" "$vtk_src/IO/PLY/vtkPLY.cxx" <<'PY'
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

# CMake names archive members after the source file. Replacing them in place
# keeps the archive in F3D's imported VTK::IOPLY link line.
ioply=$(ls $vtk_build/lib/libvtkIOPLY-*.a)
mkdir -p /work/obj
for name in vtkPLY vtkPLYReader; do
  llvm-ar t "$ioply" | grep -qx "$name.cxx.o"
  eval "$cxx $common -DNDEBUG $ply_flags -c $vtk_src/IO/PLY/$name.cxx -o /work/obj/$name.cxx.o"
done
llvm-ar rs "$ioply" /work/obj/vtkPLY.cxx.o /work/obj/vtkPLYReader.cxx.o

# The pinned release relies on transitive standard headers in several
# translation units, so the F3D build preincludes the missing ones.
cmake -S /work -B $f3d_build -G 'Unix Makefiles' \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=$cc -DCMAKE_CXX_COMPILER=$cxx \
  -DCMAKE_CXX_FLAGS='-include algorithm -include vector' \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF \
  -DVTK_DIR=$vtk_build -DPARSARIUM_F3D_SOURCE=$f3d_src \
  -DF3D_BUILD_APPLICATION=OFF -DF3D_PLUGINS_STATIC_BUILD=ON \
  -DF3D_PLUGIN_BUILD_HDF=OFF -DF3D_MODULE_UI=OFF -DF3D_MODULE_DMON=OFF \
  -DF3D_MODULE_TINYFILEDIALOGS=OFF -DF3D_MODULE_CLIP=OFF \
  -DF3D_MODULE_EXR=OFF -DF3D_MODULE_WEBP=OFF -DF3D_MODULE_FFMPEG=OFF \
  -DF3D_MODULE_RAYTRACING=OFF \
  -DPARSARIUM_INSTRUMENT="$common" \
  -DPARSARIUM_REPLAY_LINK="$link" -DPARSARIUM_FUZZER_LINK="$fuzz_link"
cmake --build $f3d_build --target replay fuzzer -j "$jobs"
cp $f3d_build/replay $f3d_build/fuzzer /work/

# Confirm that the plugin and harness compile commands carry instrumentation.
python3 - "$f3d_build/compile_commands.json" <<'PY'
import json
import sys

entries = json.load(open(sys.argv[1]))
wanted = ("/plugins/native/plugin.cxx", "/plugins/native/module/vtkF3DPLYReader.cxx",
          "/work/harness.cpp")
for suffix in wanted:
    hits = [e for e in entries if e["file"].endswith(suffix)]
    if not hits or not all("-fcoverage-mapping" in (e.get("command") or " ".join(e["arguments"]))
                           for e in hits):
        raise SystemExit(f"uninstrumented or missing: {suffix}")
PY
