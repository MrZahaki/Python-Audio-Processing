
cmake_minimum_required(VERSION 3.20)

project(sudio LANGUAGES CXX)


# Set C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS OFF)
set(CMAKE_VERBOSE_MAKEFILE OFF)
set(CMAKE_SUPPRESS_REGENERATION ON)
set_property(GLOBAL PROPERTY RULE_MESSAGES OFF)
set(CMAKE_RULE_MESSAGES OFF)
set(CMAKE_TEST_OUTPUT OFF)
set(CMAKE_INSTALL_MESSAGE NEVER)


enable_language(C)
enable_language(CXX)

if (POLICY CMP0094)
    cmake_policy(SET CMP0094 NEW)
endif()

if (NOT DEFINED Python_FIND_REGISTRY)
    set(Python_FIND_REGISTRY "LAST")
endif()
if (NOT DEFINED Python_FIND_FRAMEWORK)
    set(Python_FIND_FRAMEWORK "LAST")
endif()

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

message(STATUS "Python_EXECUTABLE: ${Python_EXECUTABLE}")
message(STATUS "Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
message(STATUS "Python_LIBRARIES: ${Python_LIBRARIES}")

list(PREPEND CMAKE_PREFIX_PATH ${Python_PREFIX})


include(FetchContent)
if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/.cache/pybind11")
    message(STATUS "Fetching pybind11...")
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11
        GIT_TAG v2.13.6
    )
    FetchContent_MakeAvailable(pybind11)
else()
    message(STATUS "Using existing pybind11 in ${CMAKE_CURRENT_SOURCE_DIR}/.cache/pybind11")
    add_subdirectory(".cache/pybind11")
endif()


include_directories(${PYTHON_INCLUDE_DIRS})
add_subdirectory(sudio/rateshift)
add_subdirectory(sudio/io)
