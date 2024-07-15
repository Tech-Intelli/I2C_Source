#pragma once

#include <pybind11/pybind11.h>
#include <memory>

namespace py = pybind11;

class ImagePipelineInterface {
public:
    virtual ~ImagePipelineInterface() = default;

    virtual py::object getImageCaptionPipeline() = 0;
    virtual py::object getImageProcessor() = 0;
};

PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
