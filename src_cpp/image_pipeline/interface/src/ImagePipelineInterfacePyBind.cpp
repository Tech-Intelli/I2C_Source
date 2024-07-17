#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "ImagePipelineInterface.h"
#include "Blip2Pipeline.h"

namespace py = pybind11;

PYBIND11_MODULE(image_pipeline, m) {
    py::class_<ImagePipelineInterface, std::shared_ptr<ImagePipelineInterface>>(m, "ImagePipelineInterface")
        .def("get_image_caption_pipeline", &ImagePipelineInterface::getImageCaptionPipeline)
        .def("get_image_processor", &ImagePipelineInterface::getImageProcessor);

    py::class_<Blip2Pipeline, ImagePipelineInterface, std::shared_ptr<Blip2Pipeline>>(m, "Blip2Pipeline")
        .def(py::init<>());
}
