cmake_minimum_required(VERSION 3.18)
set(CMAKE_CXX_STANDARD 14)
project(PatternScopeAI)
set(SOURCE_ROOT ${CMAKE_CURRENT_LIST_DIR})

file(GLOB_RECURSE SOURCES 
    ${SOURCE_ROOT}/src/ai/*.cpp
    ${SOURCE_ROOT}/src/data/*.cpp
)

add_executable(patternScopeAI src/main.cpp ${SOURCES})
target_include_directories(patternScopeAI PRIVATE ${SOURCE_ROOT}/src)

add_executable(test_all test_all.cpp ${SOURCES})
target_include_directories(test_all PRIVATE ${SOURCE_ROOT}/src)

add_executable(trainer src/trainer.cpp ${SOURCES})
target_include_directories(trainer PRIVATE ${SOURCE_ROOT}/src)

add_executable(predictor src/predictor.cpp ${SOURCES})
target_include_directories(predictor PRIVATE ${SOURCE_ROOT}/src)
