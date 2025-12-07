cmake_minimum_required(VERSION 3.18)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(PatternScopeAI)

set(SOURCE_ROOT ${CMAKE_CURRENT_LIST_DIR})
set(CMAKE_CURRENT_SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR})

file(GLOB_RECURSE ALL_SOURCES 
    ${SOURCE_ROOT}/src/*.cpp
    ${SOURCE_ROOT}/src/*.h
)

# Exclude GUI files from main executable
list(FILTER ALL_SOURCES EXCLUDE REGEX ".*gui/.*")
set(SOURCES ${ALL_SOURCES})

file(GLOB_RECURSE LIB_SOURCES 
    ${SOURCE_ROOT}/src/data/*.cpp
    ${SOURCE_ROOT}/src/data/*.h
    ${SOURCE_ROOT}/src/ai/*.cpp
    ${SOURCE_ROOT}/src/ai/*.h
)

add_executable(patternScopeAI ${SOURCES})
target_include_directories(patternScopeAI PRIVATE ${SOURCE_ROOT}/src)

add_executable(test_all test_all.cpp ${LIB_SOURCES})
target_include_directories(test_all PRIVATE ${SOURCE_ROOT})

