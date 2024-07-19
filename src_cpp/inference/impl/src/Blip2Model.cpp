#include <iostream>
#include "Blip2Model.h"
#include <opencv2/opencv.hpp>

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
    std::cout << "Loading model: " << std::endl;

    return py::none();
}

std::string Blip2Model::getDevice() const
{
    return "CPU";
}

cv::Mat Blip2Model::loadImage(const std::string &image_path)
{
    std::cout << "Loading image: " << image_path << std::endl;

    cv::Mat image = cv::imread(image_path);

    if (image.empty())
    {
        throw std::runtime_error("Failed to open image file: " + image_path);
    }
    cv::cvtColor(image, image, cv::COLOR_BGR2RGB);
    return image;
}

void Blip2Model::getImageCaptionPipeline(const std::string &image_path)
{
    std::cout << "Loading image: " << image_path << std::endl;
}
