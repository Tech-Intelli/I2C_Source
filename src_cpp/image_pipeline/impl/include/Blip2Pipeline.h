#pragma once

#include "ImagePipelineInterface.h"

class Blip2Pipeline : public ImagePipelineInterface {
public:
    Blip2Pipeline();

    py::object getImageCaptionPipeline() override;
    py::object getImageProcessor() override;

private:
    static void initializeBlip2();
    
    static py::object model;
    static py::object processor;
};
