cmake_minimum_required(VERSION 3.23)
project(parsarium_trilinos_reader LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(TeuchosNumerics CONFIG REQUIRED)

add_executable(parsarium_trilinos ../trilinos.cpp)
set_target_properties(parsarium_trilinos PROPERTIES OUTPUT_NAME trilinos)
target_link_libraries(parsarium_trilinos PRIVATE TeuchosNumerics::all_libs)
