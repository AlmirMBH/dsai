cmake_minimum_required(VERSION 3.18)

set(CMAKE_CXX_STANDARD 14)
project(PatternScopeAI)
set(SOLUTION_NAME PatternScopeAI)
set(SOURCE_ROOT ${CMAKE_CURRENT_LIST_DIR})

if(APPLE)
	set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Mac OS X build architectures" FORCE)
endif()

if(WIN32 AND "$ENV{HOME}" STREQUAL "")
	set(HOME_ROOT $ENV{USERPROFILE})
else()
	set(HOME_ROOT $ENV{HOME})
endif()
if(WIN32)
	string(REPLACE "\\" "/" HOME_ROOT "${HOME_ROOT}")
endif()
set(WORK_ROOT ${HOME_ROOT}/Work)

if(EXISTS ${WORK_ROOT}/DevEnv/Common.cmake)
	include(${WORK_ROOT}/DevEnv/Common.cmake)
	include(${WORK_ROOT}/DevEnv/natGUI.cmake)
endif()

file(GLOB_RECURSE SOURCES 
    ${SOURCE_ROOT}/src/ai/*.cpp
    ${SOURCE_ROOT}/src/data/*.cpp
    ${SOURCE_ROOT}/src/core/*.cpp
)

add_executable(patternScopeAI_cli src/main.cpp ${SOURCES})
target_include_directories(patternScopeAI_cli PRIVATE ${SOURCE_ROOT}/src)

add_executable(trainer src/trainer.cpp ${SOURCES})
target_include_directories(trainer PRIVATE ${SOURCE_ROOT}/src)

add_executable(predictor src/predictor.cpp ${SOURCES})
target_include_directories(predictor PRIVATE ${SOURCE_ROOT}/src)

if(EXISTS ${WORK_ROOT}/DevEnv/Common.cmake)
	include(patternScopeAI.cmake)
endif()

set(RESOURCES_SRC ${SOURCE_ROOT}/resources)
set(_PV_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}")

# For GUI app bundle on macOS: bundle layout and GUI resources (res, Theme); data lives in source resources/
if(APPLE)
  add_custom_command(TARGET ${APP_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory $<TARGET_FILE_DIR:${APP_NAME}>/../Resources
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${SOURCE_ROOT}/res $<TARGET_FILE_DIR:${APP_NAME}>/../Resources/res
    COMMAND ${CMAKE_COMMAND} -E copy ${SOURCE_ROOT}/res/DevRes.xml $<TARGET_FILE_DIR:${APP_NAME}>/../Resources/DevRes.xml
    COMMAND ${CMAKE_COMMAND} -E copy ${SOURCE_ROOT}/res/main.xml $<TARGET_FILE_DIR:${APP_NAME}>/../Resources/main.xml
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${SOURCE_ROOT}/res/tr $<TARGET_FILE_DIR:${APP_NAME}>/../Resources/tr
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${SOURCE_ROOT}/Theme $<TARGET_FILE_DIR:${APP_NAME}>/../Resources/Theme
    COMMAND /bin/sh -c "ln -snf Theme '$<TARGET_FILE_DIR:${APP_NAME}>/../Resources/Work'"
    COMMAND ${CMAKE_COMMAND} -E rename $<TARGET_FILE_DIR:${APP_NAME}>/PatternVision $<TARGET_FILE_DIR:${APP_NAME}>/PatternVision.bin
    COMMAND ${CMAKE_COMMAND} -E copy ${SOURCE_ROOT}/launcher.sh $<TARGET_FILE_DIR:${APP_NAME}>/PatternVision
    COMMAND chmod +x $<TARGET_FILE_DIR:${APP_NAME}>/PatternVision
    COMMENT "Copying resources into app bundle Contents/Resources"
  )
endif()
