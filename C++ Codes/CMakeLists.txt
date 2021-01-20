cmake_minimum_required(VERSION 3.5)

#project(Test_pybind LANGUAGES CXX)
project("Test_pybind")
#add_executable(Test_pybind main.cpp)

set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(APP_SOURCE "${PROJECT_SOURCE_DIR}/source/app")
set(MODULE_SOURCE "${PROJECT_SOURCE_DIR}/source/module")
set(EXTERNALS "${PROJECT_SOURCE_DIR}/externals")

# pybind11
add_subdirectory(${EXTERNALS}/pybind11)

# module
pybind11_add_module (moduleAI ${MODULE_SOURCE}/module.cpp)


target_include_directories (moduleAI PRIVATE ${MODULE_SOURCE})

# app

add_executable(pybind11app ${APP_SOURCE}/app.cpp ${MODULE_SOURCE}/piece.cpp ${MODULE_SOURCE}/piece.h ${MODULE_SOURCE}/damier.cpp ${MODULE_SOURCE}/damier.h ${MODULE_SOURCE}/engine.cpp ${MODULE_SOURCE}/engine.h)

target_include_directories (pybind11app PRIVATE ${APP_SOURCE} PRIVATE ${MODULE_SOURCE})

target_link_libraries (pybind11app PRIVATE pybind11::embed)

target_compile_definitions(moduleAI PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
