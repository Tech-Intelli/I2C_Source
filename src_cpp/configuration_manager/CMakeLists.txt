cmake_minimum_required(VERSION 3.10)
project(ConfigurationManager)

set(CMAKE_CXX_STANDARD 17)

find_package(yaml-cpp REQUIRED)

include_directories(include)

set(SOURCES
    src/ConfigManager.cpp
    src/ConfigModels.cpp
    src/main.cpp
)

add_executable(ConfigurationManager ${SOURCES})

target_link_libraries(ConfigurationManager yaml-cpp)
