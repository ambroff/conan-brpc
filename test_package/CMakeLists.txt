project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(brpc REQUIRED)

add_executable(test_package test_package.cpp)
target_link_libraries(test_package brpc::brpc)
