cmake_minimum_required(VERSION 3.10)
project(PromptProcessor)

set(CMAKE_CXX_STANDARD 17)

find_package(spdlog REQUIRED)

include_directories(include)

set(SOURCES
    main.cpp
    PromptStrategy.cpp
    InstagramStrategy.cpp
    FacebookStrategy.cpp
    TwitterStrategy.cpp
    LinkedinStrategy.cpp  
    TiktokStrategy.cpp
)

add_executable(PromptProcessor ${SOURCES})

target_link_libraries(PromptProcessor spdlog::spdlog)