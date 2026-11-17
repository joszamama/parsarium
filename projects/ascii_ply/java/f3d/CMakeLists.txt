cmake_minimum_required(VERSION 3.21)
project(parsarium_f3d_java_ply LANGUAGES C CXX)

# Configure the pinned F3D tree as a subproject so its own Java binding
# targets (javaf3d, f3d-jar) link libf3d and the static native plugin.
set(PARSARIUM_F3D_SOURCE "" CACHE PATH "Pinned F3D source tree")
set(PARSARIUM_INSTRUMENT "" CACHE STRING "LLVM coverage compile flags")
add_subdirectory("${PARSARIUM_F3D_SOURCE}" f3d)

separate_arguments(instrument UNIX_COMMAND "${PARSARIUM_INSTRUMENT}")

# javaf3d compiles the JNI bindings (java/F3D*Bindings.cxx). f3d-plugin-native
# compiles plugin.cxx, which includes the generated reader_PLYReader.h and
# plugins/native/ply.inl. f3d::vtkextNative compiles vtkF3DPLYReader.cxx.
# Only these F3D targets carry LLVM coverage; build-native.sh swaps the
# instrumented VTK vtkPLY and vtkPLYReader objects into libvtkIOPLY.
if(NOT TARGET javaf3d)
  message(FATAL_ERROR "F3D Java binding target javaf3d not found")
endif()
get_target_property(native_module f3d::vtkextNative ALIASED_TARGET)
if(NOT native_module)
  message(FATAL_ERROR "f3d::vtkextNative module target not found")
endif()
foreach(target IN ITEMS javaf3d f3d-plugin-native ${native_module})
  target_compile_options(${target} PRIVATE ${instrument})
endforeach()
target_link_options(javaf3d PRIVATE -fprofile-instr-generate)
