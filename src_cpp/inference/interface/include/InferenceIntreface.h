/**
 * @brief Defines an abstract class for inference operations.
 * 
 * This class serves as an interface for performing inference tasks such as
 * generating image captions and loading models. Subclasses must implement
 * the getImageCaption and loadModel methods. The 'collection' attribute is
 * protected and can be accessed by subclasses.
 */
#ifndef INFERENCE_ABSTRACT_H
#define INFERENCE_ABSTRACT_H

#include <string>

class InferenceAbstract {
public:
    virtual ~InferenceAbstract() {}
    virtual std::string getImageCaption(const std::string& imagePath) = 0;
    virtual void loadModel() = 0;

protected:
    std::string collection;
};

#endif
