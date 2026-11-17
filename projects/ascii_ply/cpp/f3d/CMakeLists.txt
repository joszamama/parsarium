cmake_minimum_required(VERSION 3.21)
project(parsarium_f3d_ply LANGUAGES C CXX)

# Configure the pinned F3D tree as a subproject so the harness links libf3d
# and its static native plugin through F3D's own usage requirements.
set(PARSARIUM_F3D_SOURCE "" CACHE PATH "Pinned F3D source tree")
set(PARSARIUM_INSTRUMENT "" CACHE STRING "Coverage and sanitizer compile flags")
set(PARSARIUM_REPLAY_LINK "" CACHE STRING "Link flags for the replay binary")
set(PARSARIUM_FUZZER_LINK "" CACHE STRING "Link flags for the libFuzzer binary")
add_subdirectory("${PARSARIUM_F3D_SOURCE}" f3d)

separate_arguments(instrument UNIX_COMMAND "${PARSARIUM_INSTRUMENT}")
separate_arguments(replay_link UNIX_COMMAND "${PARSARIUM_REPLAY_LINK}")
separate_arguments(fuzzer_link UNIX_COMMAND "${PARSARIUM_FUZZER_LINK}")

# f3d-plugin-native compiles plugin.cxx, which includes the generated
# reader_PLYReader.h and plugins/native/ply.inl. f3d::vtkextNative compiles
# vtkF3DPLYReader.cxx. Only these F3D targets carry coverage and sanitizers.
get_target_property(native_module f3d::vtkextNative ALIASED_TARGET)
if(NOT native_module)
  message(FATAL_ERROR "f3d::vtkextNative module target not found")
endif()
foreach(target IN ITEMS f3d-plugin-native ${native_module})
  target_compile_options(${target} PRIVATE ${instrument})
endforeach()

add_executable(replay replay.cpp harness.cpp)
add_executable(fuzzer fuzz.cpp harness.cpp)
foreach(target IN ITEMS replay fuzzer)
  set_target_properties(${target} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED ON)
  target_compile_options(${target} PRIVATE ${instrument})
  target_link_libraries(${target} PRIVATE libf3d)
endforeach()
target_link_options(replay PRIVATE ${replay_link})
target_link_options(fuzzer PRIVATE ${fuzzer_link})
