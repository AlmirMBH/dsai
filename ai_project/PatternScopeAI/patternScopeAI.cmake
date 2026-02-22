set(APP_NAME PatternVision)

# Collect GUI sources and headers
file(GLOB GUI_SOURCES ${CMAKE_CURRENT_LIST_DIR}/src/gui/*.cpp)
file(GLOB GUI_MM ${CMAKE_CURRENT_LIST_DIR}/src/gui/*.mm)
list(APPEND GUI_SOURCES ${GUI_MM})
file(GLOB GUI_INCS ${CMAKE_CURRENT_LIST_DIR}/src/gui/*.h)
set(APP_PLIST ${CMAKE_CURRENT_LIST_DIR}/src/Info.plist)

# Define the GUI application
# Note: GUI_SOURCES already includes src/gui/main.cpp
add_executable(${APP_NAME} ${GUI_SOURCES} ${GUI_INCS} ${SOURCES})

target_include_directories(${APP_NAME} PRIVATE ${SOURCE_ROOT}/src)

target_link_libraries(${APP_NAME} 
    debug ${MU_LIB_DEBUG} debug ${NATGUI_LIB_DEBUG}
    optimized ${MU_LIB_RELEASE} optimized ${NATGUI_LIB_RELEASE})
if(APPLE)
  target_link_libraries(${APP_NAME} "-framework Foundation" "-framework CoreFoundation" "-framework AppKit")
endif()

setTargetPropertiesForGUIApp(${APP_NAME} ${APP_PLIST})
setIDEPropertiesForGUIExecutable(${APP_NAME} ${CMAKE_CURRENT_LIST_DIR})
setPlatformDLLPath(${APP_NAME})
