cmake_minimum_required(VERSION 3.18)

# Override architecture for ARM64 BEFORE including Common.cmake
set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Mac OS X build architectures" FORCE)

set(CMAKE_CXX_STANDARD 14)
project(PatternScopeAI)

set(SOURCE_ROOT ${CMAKE_CURRENT_LIST_DIR})
set(HOME_ROOT $ENV{HOME})
if (WIN32)
	string(REPLACE "\\" "/" HOME_ROOT "${HOME_ROOT}")
endif()
set(WORK_ROOT ${HOME_ROOT}/Work)

include(${WORK_ROOT}/DevEnv/Common.cmake)
include(${WORK_ROOT}/DevEnv/natGUI.cmake)

file(GLOB_RECURSE SOURCES 
    ${SOURCE_ROOT}/src/ai/*.cpp
    ${SOURCE_ROOT}/src/data/*.cpp
)

add_executable(patternScopeAI_cli src/main.cpp ${SOURCES})
target_include_directories(patternScopeAI_cli PRIVATE ${SOURCE_ROOT}/src)

add_executable(test_all test_all.cpp ${SOURCES})
target_include_directories(test_all PRIVATE ${SOURCE_ROOT}/src)

add_executable(trainer src/trainer.cpp ${SOURCES})
target_include_directories(trainer PRIVATE ${SOURCE_ROOT}/src)

add_executable(predictor src/predictor.cpp ${SOURCES})
target_include_directories(predictor PRIVATE ${SOURCE_ROOT}/src)

include(patternScopeAI.cmake)
