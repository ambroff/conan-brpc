cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

# TODO: move to conandata.yml
set(BRPC_REVISION "46d8ee99c")

# we need to set the executable manually since that seems to be missing in
# the generated FindProtobuf.cmake; this is also related to the misplaced
# endif in the protobuf recipe
find_program(PROTOBUF_PROTOC_EXECUTABLE NAMES protoc)
# oddly, brpc uses both variants of protobuf include directories
set(PROTOBUF_INCLUDE_DIRS "${CONAN_PROTOBUF_ROOT}/include")
set(PROTOBUF_INCLUDE_DIR "${CONAN_PROTOBUF_ROOT}/include")

# disable picking up system-installed libraries with find_library
set(CMAKE_FIND_USE_CMAKE_SYSTEM_PATH FALSE)

add_subdirectory(incubator-brpc-1.3.0)
