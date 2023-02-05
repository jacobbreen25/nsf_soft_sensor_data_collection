cmake_minimum_required(VERSION 3.7)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(
    nsf_soft_sensor_application
)
include (FetchContent)
#FetchContent_Declare(mahi-gui GIT_REPOSITORY https://github.com/jacobbreen25/mahi-gui.git) 
#FetchContent_MakeAvailable(mahi-gui)

#FetchContent_GetProperties(simpleble)
#if(NOT simpleble_POPULATED)
#    FetchContent_Populate(simpleble)
#    list(APPEND CMAKE_MODULE_PATH "${simpleble_SOURCE_DIR}/cmake/find")
#    add_subdirectory("${simpleble_SOURCE_DIR}/simpleble" "${simpleble_BINARY_DIR}")
#endif()

#set(simpleble_FOUND 1)

add_subdirectory("${CMAKE_BINARY_DIR}/include/SimpleBLE-main/simpleble" "${CMAKE_BINARY_DIR}/simpleble")

add_executable(app app.cpp)
#target_link_libraries(app mahi::gui)
target_link_libraries(app simpleble::simpleble)
#target_include_directories(app PUBILC "${PROJECT_BINARY_DIR}"
#"${PROJECT_SOURCE_DIR} common"
#)