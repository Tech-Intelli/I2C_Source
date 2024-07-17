#include "Blip2Pipeline.h"
#include "ConfigManager.h"
#include <pybind11/pybind11.h>
#include <pybind11/embed.h>

namespace py = pybind11;
using namespace pybind11::literals;

py::object Blip2Pipeline::model = py::none();
py::object Blip2Pipeline::processor = py::none();

Blip2Pipeline::Blip2Pipeline() {
    initializeBlip2();
}

void Blip2Pipeline::initializeBlip2() {
    if (!model.is_none()) {
        return;
    }

    py::module_ torch = py::module_::import("torch");
    py::module_ transformers = py::module_::import("transformers");
    auto config_manager = ConfigManager::getInstance("../../configuration_manager/config.yaml");
    auto config = config_manager->getAppConfig().multimodal.blip;

    py::object BitsAndBytesConfig = transformers.attr("BitsAndBytesConfig");
    py::object Blip2ForConditionalGeneration = transformers.attr("Blip2ForConditionalGeneration");
    py::object AutoProcessor = transformers.attr("AutoProcessor");

    py::object quantization_config = BitsAndBytesConfig(py::dict(
        "load_in_8bit"_a=true,
        "llm_int8_threshold"_a=5.0));
    model = Blip2ForConditionalGeneration.attr("from_pretrained")(
        config,
        py::arg("torch_dtype") = torch.attr("float16"),
        py::arg("device_map") = "auto",
        py::arg("quantization_config") = quantization_config);
    processor = AutoProcessor.attr("from_pretrained")(config);
}

py::object Blip2Pipeline::getImageCaptionPipeline() {
    initializeBlip2();
    return model;
}

py::object Blip2Pipeline::getImageProcessor() {
    initializeBlip2();
    return processor;
}
