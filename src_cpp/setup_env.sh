#!/bin/bash

# Set Python3 paths
export Python3_ROOT_DIR="/usr"
export Python3_EXECUTABLE="/usr/bin/python3.10"
export Python3_INCLUDE_DIR="/usr/include/python3.10"
export Python3_LIBRARY="/usr/lib/x86_64-linux-gnu/libpython3.10.so"

export YAML_CPP_INCLUDE_DIRS="/usr/include/yaml-cpp"
export YAML_CPP_LIBRARIES="/usr/lib/x86_64-linux-gnu/libyaml-cpp.so"

echo "Python3_ROOT_DIR: ${Python3_ROOT_DIR}"
echo "Python3_EXECUTABLE: ${Python3_EXECUTABLE}"
echo "Python3_INCLUDE_DIR: ${Python3_INCLUDE_DIR}"
echo "Python3_LIBRARY: ${Python3_LIBRARY}"
echo "YAML_CPP_INCLUDE_DIRS: ${YAML_CPP_INCLUDE_DIRS}"
echo "YAML_CPP_LIBRARIES: ${YAML_CPP_LIBRARIES}"

mkdir -p build
cd build

cmake .. -DPython3_ROOT_DIR=${Python3_ROOT_DIR} \
         -DPython3_EXECUTABLE=${Python3_EXECUTABLE} \
         -DPython3_INCLUDE_DIR=${Python3_INCLUDE_DIR} \
         -DPython3_LIBRARY=${Python3_LIBRARY} \
         -DYAML_CPP_INCLUDE_DIRS=${YAML_CPP_INCLUDE_DIRS} \
         -DYAML_CPP_LIBRARIES=${YAML_CPP_LIBRARIES}

make
