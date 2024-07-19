/**
 * @brief Defines an abstract class for inference operations.
 * 
 * This class serves as an interface for performing inference tasks such as
 * generating image captions and loading models. Subclasses must implement
 * the getImageCaption and loadModel methods. The 'collection' attribute is
 * protected and can be accessed by subclasses.
 */
#ifndef INFERENCE_INTERFACE_H
#define INFERENCE_INTERFACE_H

#include <string>
#include <pybind11/pybind11.h>
#include <opencv2/opencv.hpp>

namespace py = pybind11;
class InferenceInterface {
public:
    InferenceInterface(const std::string& collection)
        : m_collection(collection) {}
    virtual ~InferenceInterface() {}
    virtual std::string getImageCaption(const std::string& imagePath) = 0;
    virtual py::object loadModel() = 0;
    virtual std::string getDevice() const = 0;
    virtual cv::Mat loadImage(const std::string& image_path) = 0;
    virtual void getImageCaptionPipeline(const std::string& image_path) = 0;
protected:
    std::string m_collection;
};

#endif // INFERENCE_INTERFACE_H
