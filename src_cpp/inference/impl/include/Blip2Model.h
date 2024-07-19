#pragma once
#ifndef BLIP2_MODEL_H
#define BLIP2_MODEL_H

#include "ImagePipelineInterface.h"
#include "InferenceInterface.h"
#include <memory>

namespace py = pybind11;

class ImagePipelineInterface;

class Blip2Model : public InferenceInterface {
public:
    Blip2Model(const std::string& collection);
    ~Blip2Model();

    std::string getImageCaption(const std::string& imagePath) override;
    py::object loadModel() override;
    std::string getDevice() const override;
    void loadImage(const std::string& image_path) override;
    void getImageCaptionPipeline(const std::string& image_path) override;

private:
    std::shared_ptr<ImagePipelineInterface> m_imagePipeline;
    std::string m_collection;
};

#endif // BLIP2_MODEL_H
