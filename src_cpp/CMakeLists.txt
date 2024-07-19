cmake_minimum_required(VERSION 3.10)
project(ImagePipelineProject)

set(CMAKE_CXX_STANDARD 17)

# Find pybind11
find_package(pybind11 REQUIRED)

# Find Python3, allowing hints from the environment
find_package(Python3 3.10 REQUIRED COMPONENTS Interpreter Development)

# Find YAML-cpp
find_package(yaml-cpp REQUIRED)

# Optionally print the Python paths to debug
message(STATUS "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
message(STATUS "Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
message(STATUS "Python3_LIBRARIES: ${Python3_LIBRARIES}")
message(STATUS "YAML-CPP_INCLUDE_DIRS: ${YAML_CPP_INCLUDE_DIRS}")
message(STATUS "YAML-CPP_LIBRARIES: ${YAML_CPP_LIBRARIES}")

include_directories(
    ${Python3_INCLUDE_DIRS}
    ${YAML_CPP_INCLUDE_DIRS}
    configuration_manager/include
    image_pipeline/interface/include
    image_pipeline/impl/include
    inference/interface/include
    inference/impl/include
)

# Add the shared library for the image pipeline interface
add_library(image_pipeline_interface SHARED
    image_pipeline/interface/src/ImagePipelineInterfacePyBind.cpp
    image_pipeline/impl/src/Blip2Pipeline.cpp
    inference/impl/src/Blip2Model.cpp
)

# Add the executable for the main program
add_executable(main_exe 
    configuration_manager/src/ConfigManager.cpp 
    configuration_manager/src/ConfigModels.cpp
    configuration_manager/src/main.cpp
)

# Link the pybind11 module and embedding library to the shared library
target_link_libraries(image_pipeline_interface PRIVATE pybind11::module pybind11::embed Python3::Python)

# Link the shared library and pybind11 embedding library to the main executable
target_link_libraries(main_exe PRIVATE image_pipeline_interface pybind11::embed Python3::Python ${YAML_CPP_LIBRARIES})
