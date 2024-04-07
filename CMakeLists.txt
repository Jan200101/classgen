cmake_minimum_required(VERSION 3.25)

project(classgen LANGUAGES C CXX)

list(
    APPEND
    CMAKE_MODULE_PATH
    "${PROJECT_SOURCE_DIR}/cmake"
    )
include(classgen)

convert_class("${CMAKE_CURRENT_SOURCE_DIR}/class.hpp" "output_dir")
message(STATUS "${output_dir}")
include_directories(${output_dir})

add_executable(test_cpp test.cpp)
add_executable(test_c test.c)