#include <iostream>
#include "Blip2Model.h"

namespace py = pybind11;
using namespace pybind11::literals;
Blip2Model::Blip2Model(const std::string &collection) : InferenceInterface(collection)
{
}

Blip2Model::~Blip2Model()
{
}

std::string Blip2Model::getImageCaption(const std::string &imagePath)
{
    return std::string();
}

py::object Blip2Model::loadModel()
{
    return py::none();
}

std::string Blip2Model::getDevice() const
{
    return "CPU";
}

void Blip2Model::loadImage(const std::string &image_path)
{
    std::cout << "Loading image: " << image_path << std::endl;
}

void Blip2Model::getImageCaptionPipeline(const std::string &image_path)
{
    std::cout << "Loading image: " << image_path << std::endl;
}
