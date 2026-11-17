#!/bin/sh
set -eu
# Minimal JUCE module set for Drawable::createFromSVGFile: juce_core,
# juce_events, and juce_graphics (which bundles the LunaSVG parser). No GUI,
# audio, or juceaide. WebP, fontconfig, and curl are off; none is on the SVG
# document path. The module objects carry LLVM coverage and are linked into
# both the replay and the fuzzer.
modules=/work/source/modules
defines='-DNDEBUG=1 -DJUCE_GLOBAL_MODULE_SETTINGS_INCLUDED=1 -DJUCE_STANDALONE_APPLICATION=1
 -DJUCE_MODULE_AVAILABLE_juce_core=1 -DJUCE_MODULE_AVAILABLE_juce_events=1 -DJUCE_MODULE_AVAILABLE_juce_graphics=1
 -DJUCE_USE_CURL=0 -DJUCE_WEB_BROWSER=0 -DJUCE_USE_WEBP=0 -DJUCE_USE_FONTCONFIG=0'
common="-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping $defines -I$modules $(pkg-config --cflags freetype2)"
mkdir -p /work/build
for unit in juce_core/juce_core.cpp juce_core/juce_core_CompilationTime.cpp juce_events/juce_events.cpp \
  juce_graphics/juce_graphics.cpp juce_graphics/juce_graphics_Harfbuzz.cpp; do
  clang++ -std=c++17 $common -c "$modules/$unit" -o "/work/build/$(basename "$unit").o" &
done
wait
for unit in juce_core/juce_core_zlib.c juce_graphics/juce_graphics_Sheenbidi.c juce_graphics/juce_graphics_libjpg_1.c \
  juce_graphics/juce_graphics_libjpg_2.c juce_graphics/juce_graphics_libjpg_3.c juce_graphics/juce_graphics_libpng.c \
  juce_graphics/juce_graphics_lunasvg.c; do
  clang $common -c "$modules/$unit" -o "/work/build/$(basename "$unit").o" &
done
wait
for unit in juce_core.cpp juce_core_CompilationTime.cpp juce_events.cpp juce_graphics.cpp juce_graphics_Harfbuzz.cpp \
  juce_core_zlib.c juce_graphics_Sheenbidi.c juce_graphics_libjpg_1.c juce_graphics_libjpg_2.c juce_graphics_libjpg_3.c \
  juce_graphics_libpng.c juce_graphics_lunasvg.c; do
  test -s "/work/build/$unit.o"
done
harness="-std=c++17 -O1 -g -fno-omit-frame-pointer $defines -I$modules $(pkg-config --cflags freetype2)"
libs="/work/build/*.o $(pkg-config --libs freetype2) -lpthread -ldl -lrt"
clang++ $harness -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp $libs -o /work/replay
clang++ $harness -fprofile-instr-generate -fsanitize=fuzzer,address,undefined /work/harness.cpp $libs -o /work/fuzzer
